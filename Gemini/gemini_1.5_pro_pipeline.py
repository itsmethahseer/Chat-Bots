example_json_structure = """
        {
  "header": {
    "invoice_number": "string",
    "invoice_date": "string",
    "due_date": "string",
    "currency": "string"
  },
  "customer": {
    "name": "string",
    "address": "string",
    "city": "string",
    "country": "string",
    "postal_code": "string"
  },
  "seller": {
    "name": "string",
    "address": "string",
    "city": "string",
    "country": "string",
    "postal_code": "string"
  },
  "shipment_details": {
    "vessel_voyage": "string",
    "load_terminal": "string",
    "discharge_terminal": "string",
    "sailed_date": "string",
    "swb_number": "string"
  },
  "items": [
    {
      "item_id": "string",
      "description": "string",
      "quantity": "string",
      "unit_price": "string",
      "tax_rate": "string",
      "tax_amount": "string",
      "line_total": "string"
    }
  ],
  "totals": {
    "subtotal": "string",
    "total_tax": "string",
    "grand_total": "string"
  },
  "payment_terms": "string",
  "notes": "string"
}
"""

common_prompt = f"""Understand the invoice structure and accurately extract the following information:
                                    
                                        **General Fields:**

                                            **Invoice Number:** What is the invoice number?
                                            **Invoice Date:** When was the invoice issued?
                                            **Due Date:** When is the invoice due?
                                            **Currency:** What is the currency used in the invoice?
                                            **Customer Name:** Who is the customer?
                                            **Customer Address:** What is the customer's address?
                                            **Customer City:** What is the customer's city?
                                            **Customer Country:** What is the customer's country?
                                            **Customer Postal Code:** What is the customer's postal code?
                                            **Seller Name:** Who is the seller?
                                            **Seller Address:** What is the seller's address?
                                            **Seller City:** What is the seller's city?
                                            **Seller Country:** What is the seller's country?
                                            **Seller Postal Code:** What is the seller's postal code?

                                        **Shipment Details:**

                                            **Vessel Voyage:** What is the vessel voyage (if applicable)?
                                            **Load Terminal:** What is the load terminal (if applicable)?
                                            **Discharge Terminal:** What is the discharge terminal (if applicable)?
                                            **Sailed Date:** When did the vessel sail (if applicable)?
                                            **SWB Number:** What is the Shipping Bill of Entry (SWB) number (if applicable)?

                                        **Items:**

                                            **Item ID:** What is the item identifier?
                                            **Description:** What is the item description?
                                            **Quantity:** How many units of the item were shipped?
                                            **Unit Price:** What is the unit price of the item?
                                            **Tax Rate:** What is the tax rate applicable to the item?
                                            **Tax Amount:** What is the tax amount for the item?
                                            **Line Total:** What is the total cost of the item, including taxes?

                                        **Totals:**:

                                            **Subtotal:** What is the total cost of the items before taxes?
                                            **Total Tax:** What is the total amount of taxes?
                                            **Grand Total:** What is the total cost of the invoice, including taxes and extra charges?

                                        **Payment Terms:**:

                                            **Payment Terms:** What are the terms of payment?

                                        **Notes:**:

                                            **Notes:** Are there any additional notes or comments on the invoice?
        
                                        
        
                                        If any of these fields are missing or cannot be accurately extracted, return "NA" for the corresponding field.
                                        Please provide the results in JSON format with the following structure:
                                        {example_json_structure}

                                    Example Input Text:
                                    """



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

load_dotenv()
def extract_invoice_details(base64_data,prompt):
    global response_variable


    image_parts = [
        {
            "mime_type": "application/pdf",  # Adjust mime type if needed
            "data": base64_data
        }
    ]


    genai.configure(api_key="AIzaSyB7p-otS_WJ81mBRWJYcN0IQw_rPOC4E_8")

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
    print(response_variable)
    with open("result.txt","a") as write:
        write.write(str(response_variable))
    return response_variable




def get_result(pdf_path:str):

    #Extract invoice details
    invoice_details = extract_invoice_details(pdf_path,prompt=common_prompt)
    print(invoice_details)
    invoice_details = json.loads(invoice_details)
    print("final response",invoice_details)
    # Print or process the extracted details

    # # Optionally, save the extracted details to a JSON file
    # with open('extracted_invoice_details.json', 'w') as json_file:
    #     json.dump(invoice_details, json_file, indent=4)

    return invoice_details





        