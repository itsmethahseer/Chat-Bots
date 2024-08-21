""""Function for getting response using prompt from a pdf by passing it's base64 URI format.""
import google.generativeai as genai
import fitz
import logging
import os
from pdf2image import convert_from_path
import base64
import json
from dotenv import load_dotenv
from decrypt import decrypt
import pandas as pd
import time
from collections import defaultdict
import tempfile

example_json_structure = """
        {
          "invoices": [
            {
              "invoice_number": "string",
              "date": "string",
              "borrower_name": "string",
              "end_client_name": "string",
              "bank_name": "string",
              "account_name": "string",
              "account_number": "string",
              "ifsc_code": "string",
              "service_period": "string",
              "taxable_amount": "string",
              "grand_total": "string",
              "po_number": "string",
              "line_items": [
                { "serial_number": "string",
                  "mrp": "string",
                  "discount_percentage": "string",
                  "discount_price" : "string",
                  "tax_percentage" : "string",
                  "description": "string",
                  "hsn_sac_code": "string",
                  "quantity": "string",
                  "price": "string",
                  "value": "string"
                }
              ]
            }
          ]
        }
"""
common_prompt = f"""
                                Understand the invoice structure and accurately extract the following information:
    
                                    **General_Fields:**
    
                                        1. **Invoice_Number:** (**Improved Accuracy Focus**)
                                            - Identify and extract the unique invoice identifier, prioritizing keywords like "Invoice No.", "Invoice #", "Bill No.", or "Reference No." over keywords like "e-Way Bill No."
                                            - **Exclude Keywords**: Exclude instances where the phrases "e-Way Bill No Dated," "Invoice No. Dated," or "e-Way Bill No. Dated" are considered as the invoice number.
                                            - **Exclude Fully Alphabetic Invoice Numbers**: Avoid selecting identifiers that consist entirely of alphabets (e.g., "Invoice ABC").
                                            - **Context-Driven Search**: Look for proximity to invoice date, seller/buyer information, grand total, distinct sections, and prominent placement.
                                            - **Pattern Analysis**: Match patterns from your invoice dataset (e.g., letter-number combinations, prefixes/suffixes). Include examples like "135" as potential valid invoice number patterns.
                                            - **Example Formats**: Valid invoice numbers may include ETS/TS/JAN23/224, 2228502574, BLVAPI2223000087, 23-24/P057,. Pay attention to various combinations of letters, numbers, and symbols in the invoice number.
                                            - **Confidence Scores**: Assign scores based on keyword proximity, formatting, and pattern matching. Return multiple candidates with low scores for review.
                                            - **Exclude "Invoice No. Dated"**: Exclude instances where "Invoice No. Dated" is considered as the invoice number. If accurate extraction is not possible, return "NA".
                                            - **Example**: If the invoice number is "123456," the extraction should be "123456." If the phrase "e-Way Bill No Dated" precedes the number, do not consider it as the invoice number.
                                            - **Counter-Example**: If the identifier is fully alphabetic (e.g., "Invoice ABC"), do not extract it as the invoice number.
    
                                        2. **Date:** Recognize and extract the invoice issuance date. Look for formats like "dd/mm/yyyy", "dd-mm-yyyy", or "Month dd, yyyy". Consider context with keywords like "Issued Date", "Invoice Date", or "Date of Bill". If accurate extraction is not possible, return "NA".
    
                                        3. **Borrower_Name:** Extract the seller's name accurately. Prioritize keywords like "Seller", "Supplier", "Vendor", or "Bill From". Ensure the extracted name corresponds to the entity providing the service/goods. If accurate extraction is not possible, return "NA".
    
                                        4. **End_Client_Name:** Extract the buyer's name accurately. Look for keywords like "Buyer", "Customer", "Bill To", or "End Client". Ensure the extracted name corresponds to the entity receiving the service/goods. If accurate extraction is not possible, return "NA".
    
                                        5. **Bank_Name:**
                                            - Prioritize consistent matches across the document, including common bank names and abbreviations.
                                            - Look for logos, letterheads, or other visual cues indicating bank affiliation.
                                            - If no clear keywords are found, analyze contextual clues within payment sections for potential bank names. If accurate extraction is not possible, return "NA".
    
                                        6. **Account_Name:**
                                            - If the account name is present, extract and return it.
                                            - Ensure the extracted name contains only alphabets.
                                            - If digits are present, attempt to isolate alphabetic parts for potential account names.
                                            - Cross-check with extracted account numbers for consistency (e.g., similar name patterns).
                                            - If the account name is not found, return "NA".
    
                                        7. **Account_Number:**
                                            - Ensure the extracted format aligns with common account number patterns (e.g., alphanumeric mix, dashes).
                                            - Implement regular expressions to match specific numerical patterns with likely account numbers, considering variations like "EFSPXXXXXXXXX" or similar formats.
                                            - Provide examples of possible account number formats in your dataset, including prefixes or suffixes.
                                            - If accurate extraction is not possible, return "NA".
    
                                        8. **IFSC_Code:**
                                            - Prioritize strings containing 11 characters (alphanumeric + four-character bank code).
                                            - Validate extracted codes against a list of valid IFSC codes for accuracy. If accurate extraction is not possible, return "NA".
    
                                        9. **Service_or_Billing_Period:** Identify and extract the service/billing period. Look for keywords like "Service Period," "Billing Period," "From," and "To." Prioritize clear date ranges in the format "From [start_date] to [end_date]".
                                            - If a clear date range is not found:
                                                - Look for keywords related to the invoice date, such as "Issued Date," "Invoice Date," or "Date of Bill."
                                                - Extract the invoice date.
                                                - Look for keywords related to the due date, such as "Due Date" or "Payment Due By."
                                                - Extract the due date.
                                            - If both the invoice date and due date are extracted:
                                                - Define the service/billing period as the time span between the invoice date and the due date.
                                            - If accurate extraction is not possible, return "NA".
    
                                        10. **Taxable_Amount:** Find and extract the total amount subject to tax. Look for variations like "{{taxable_amount_keyword}}", "{{subtotal_keyword}}", or similar terms indicating the amount before taxes. Consider the following context-aware checks:
                                            - Validate that the extracted value is associated with line item prices before taxes.
                                            - Check for proximity to keywords related to tax, such as "Taxable Value," "Before Tax," or "Net Amount."
                                            - Ensure the extracted value is numerical and represents the sum of line item prices before taxes. If accurate extraction is not possible, return "NA".
    
                                        11. **Grand_Total:** Extract the final invoice amount, including variations like "{{grand_total_keyword}}", "{{total_amount_keyword}}", or "{{total_due_keyword}}". Consider the following context-aware checks:
                                            - Validate that the extracted value is inclusive of all charges, taxes, and fees.
                                            - Check for proximity to keywords related to the final payment, such as "Grand Total," "Total Amount Payable," or "Total Due."
                                            - Ensure the extracted value is numerical and represents the final payment due, inclusive of all charges. If accurate extraction is not possible, return "NA".
    
                                        12. **Purchase_Order_Number:**
                                            - Extract the PO number if available. Look for keywords like "PO Number," "Purchase Order Number," "Buyers Order Number," "Order Number," or "Buyer's Order No." in buyer details sections.
                                            - Check for fields labeled "Customer PONo" and extract alphanumeric values associated with it.
                                            - Also, consider variations like "Cust P.O:" as potential indicators for the PO number.
                                            - If not found using the initial checks, try to locate the PO number in the Goods Details section (if applicable) under the "Product Name & Desc" or similar fields.
                                            - If accurate extraction is not possible, return "NA".
    
                                    **Line_Item_Details:**
    
                                        For each item listed in the invoice, extract the following details:
    
                                        13. **Serial_Number:** Extract the serial number for each item to maintain the same order as in the Supplier Invoice. This field helps in showing the details in the same order as in the Supplier Invoice. If accurate extraction is not possible, assign serial numbers sequentially. If serial numbers are not present in the invoice and cannot be assigned sequentially, return "NA".
    
                                        14. **MRP:** Extract the Maximum Retail Price for each item if available. Look for keywords like "MRP," "Maximum Retail Price," or "List Price." If accurate extraction is not possible, return "NA".
    
                                        15. **Discount_Percentage:** 
                                            - Look for the exact keyword "Discount percentage" indicating a discount percentage.
                                            - If the keyword is found, extract the numerical value representing the discount percentage.
                                            - Ensure that the extracted value represents a valid percentage between 0 and 100.
                                            - Ensure that the discount percentage is not extracted from tax percentage fields or any other fields unrelated to discounts.
                                            - If the keyword is not found or if accurate extraction is not possible, return "NA".
    
                                        16. **Discount_Price:** 
                                            - Look for keywords indicating a discount, such as "Discount," "Discount Price," or "Discount Amount."
                                            - Extract the numerical value associated with the discount.
                                            - If multiple instances of discount are present, prioritize the one closest to the item it applies to.
                                            - If accurate extraction is not possible or if the discount price is not available, return "NA".
    
                                        17. **Tax_Percentage:** 
                                            - Look for keywords like "CGST," "SGST," "UTGST," and "IGST" to identify the section containing individual tax rates for each component.
                                            - Extract the individual tax rates for CGST, SGST, UTGST, and IGST separately from their respective sections.
                                            - Ensure the extracted rates are numerical and represent valid percentages.
                                            - If both SGST and UTGST are listed together, consider them collectively as the total tax rate.
                                            - Check for sub-fields like "Rate" under each tax component to identify the tax percentage value. If found, extract the percentage value from that sub-field.
                                            - Additionally, look for any other relevant keywords or indicators that may signify tax-related fields, such as "Tax Rate," "GST Rate," or "Tax Percentage."
                                            - If applicable, calculate the total tax percentage by summing up the extracted rates for CGST, SGST, UTGST, and IGST.
                                            - If accurate extraction is not possible, return "NA".
    
                                            Example 1:
                                            If CGST is 9%, SGST is 9%, and IGST is 18%, the total tax percentage would be 36%.
    
                                            Example 2:
                                            If CGST is 9% and SGST/UTGST is 5%, the total tax percentage would be 14%.
    
                                            If accurate extraction is not possible, return "NA".
    
    
    
                                        18. **Description_or_Nature_of_Service:** Recognize and extract a concise description of the material or service. Prioritize accurate descriptions appearing next to quantities or prices. If unclear, return "NA".
    
                                        19. **HSN_or_SAC_Code:** 
                                            - Locate and extract the HSN (Harmonized System Nomenclature) or SAC (Service Accounting Code) for each item.
                                            - Look for "HSN", "SAC", or similar keywords.
                                            - The code can be 6 or 4 digits long.
                                            - Ensure accuracy before returning the code.
                                            - **Exclude Quantity as HSN/SAC**: Implement checks to avoid extracting quantity as the HSN/SAC code.
                                            - If accurate extraction is not possible, return "NA".
                              
                                        20. **Quantity:** Identify and extract the quantity associated with each material or service.
                                            - Consider the context and proximity to other details on the invoice to ensure accurate extraction.
                                            - Ensure that the quantity is extracted specifically from the quantity field and not from the description of the materials.
    
                                        21. **Price:** Extract the unit price for each item using the following refined logic:
                                            - Look for keywords indicating the unit price, such as "Unit Price," "Price per Unit," or simply "Price."
                                            - Consider the proximity of the identified keyword to the line item details, ensuring it is related to the specific item being described.
                                            - Validate that the extracted value is reasonable as a unit price (e.g., positive numerical value).
                                            - Check for the presence of the term "kg" and "pcs" in the extracted value. If present, remove it to obtain a clean numerical value.
                                            - Extract only the numerical part of the value.
                                            - In case of ambiguity or multiple candidates, use additional context checks like the presence of associated quantities or other relevant terms.
                                            - If accurate extraction is not possible or if the extracted value is not a valid unit price, return "NA".
    
                                        22. **Value:** Understand the structure and extract the total value for each item (Total(INR)) using the following refined logic:
                                            - Look for keywords indicating the total value, such as "Total Value," "Total Amount," "Value," or "Total."
                                            - Consider the proximity of the identified keyword to the line item details, ensuring it is related to the specific item being described.
                                            - Validate that the extracted value is reasonable as a total value (e.g., positive numerical value).
                                            - Check for the presence of the term "INR" or any other currency indicators in the extracted value. If present, remove it to obtain a clean numerical value.
                                            - Ensure that the extracted value is not the same as or too close to the extracted "Taxable Amount." If there is a high similarity, consider it a false positive and return "NA."
                                            - In case of ambiguity or multiple candidates, use additional context checks like the presence of associated quantities or other relevant terms.
                                            - To handle cases where the correct value might be explicitly mentioned, check for nearby terms like "Total Invoice Amount," "Total Amount After Tax," or similar explicit indications of the final amount.
                                            - If accurate extraction is not possible, return "NA".

                                **Instructions for returning the data**
                                    To extract the Invoice Number, please look for a distinct identifier on the invoice that represents the invoice number.
                                    If any of these fields are missing or cannot be accurately extracted, return "NA" for the corresponding field.
                                    No need to return the collection if the field `Invoice_Number` is "NA".
                                    Please provide the results in JSON format
"""




load_dotenv()
def extract_invoice_details(base64_data,prompt):
    global response_variable


    image_parts = [
        {
            "mime_type": "application/pdf",  # Adjust mime type if needed
            "data": base64_data
        }
    ]


    genai.configure(api_key="apikey here")

    generation_config = genai.GenerationConfig(
        response_mime_type="application/json",
        temperature=0,
        top_k=10,
        top_p=0.01,
        
    )

    system_instruction="You are a skilled Invoice Parsing Expert. Analyze the base64 encoded pdf given and extract the required details according to the instructions."

    model = genai.GenerativeModel('gemini-1.5-pro',
                                generation_config=generation_config,
                                system_instruction=system_instruction)


    response = model.generate_content([system_instruction,image_parts[0],prompt])

    response_variable = response.text

    return response_variable




def get_result(pdf_path:str):

    #Extract invoice details
    invoice_details = extract_invoice_details(pdf_path,prompt=common_prompt)
    print(invoice_details)
    # invoice_details = json.loads(invoice_details)
    # Print or process the extracted details

    # # Optionally, save the extracted details to a JSON file
    # with open('extracted_invoice_details.json', 'w') as json_file:
    #     json.dump(invoice_details, json_file, indent=4)

    return invoice_details 





        