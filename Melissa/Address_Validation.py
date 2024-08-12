import re
import datetime
import requests
import json
import time

def read_license_key(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 1:
                regular_key = lines[0].strip()
                credit_key = lines[1].strip() if len(lines) > 1 else None
                return regular_key, credit_key
            else:
                raise ValueError("The key.txt file should contain at least one line for the key.")
    except Exception as e:
        print(f"Failed to read license keys: {e}")
        return None, None

def read_fips_codes(file_path):
    try:
        with open(file_path, 'r') as file:
            fips_dict = json.load(file)
            return fips_dict
    except Exception as e:
        print(f"Failed to read FIPS codes: {e}")
        return None

def extract_county_from_address(address):
    county_match = re.search(r'\(([^)]+) COUNTY\)', address)
    if county_match:
        return county_match.group(1).strip().upper()
    else:
        return "County not found"

def clean_address(address):
    cleaned_address = re.sub(r'\(.*?\)', '', address)
    cleaned_address = ' '.join(cleaned_address.split())
    return cleaned_address

def validate_address_with_melissa(address, license_key, fips_to_county):
    cleaned_address = clean_address(address)
    base_url = "https://property.melissadata.net/v4/WEB/LookupProperty"
    params = {
        "id": license_key,
        "t": "ValidationTest",
        "format": "json",
        "ff": cleaned_address
    }
    
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"API Response for '{cleaned_address}':\n{data}\n")
            if "Records" in data and len(data["Records"]) > 0:
                if "Parcel" in data["Records"][0] and "FIPSCode" in data["Records"][0]["Parcel"]:
                    fips_code = data["Records"][0]["Parcel"]["FIPSCode"]
                    if fips_code in fips_to_county:
                        return fips_to_county.get(fips_code)
                    else:
                        return f"Flagged: Outside MO, CO, KS ({fips_code})"
                else:
                    return "County not found in API response"
            else:
                return "County not found in API response"
        elif response.status_code == 401:
            return "API error: 401"
        else:
            return f"API error: {response.status_code}"
    except Exception as e:
        return f"API request failed: {e}"

def process_and_compare_addresses(input_file, license_keys, fips_to_county):
    try:
        with open(input_file, 'r') as infile:
            addresses = infile.read().strip().split('\n\n')

        discrepancies = []
        valid_matches = []
        api_errors = []

        for address in addresses:
            extracted_county = extract_county_from_address(address)
            validated_county = "County not found"

            for key in license_keys:
                if key:  # Ensure key is not None
                    validated_county = validate_address_with_melissa(address, key, fips_to_county)
                    if "API error: 401" in validated_county:
                        api_errors.append(address)
                        break  # Stop trying further keys if 401 error occurs
                    elif "County not found" not in validated_county:
                        break  # If we get a valid response, stop trying further keys

            if extracted_county.lower() != validated_county.lower():
                discrepancies.append(f"Address: {address.strip()}\nExtracted County: {extracted_county}\nValidated County: {validated_county}\n")
            else:
                valid_matches.append(f"Address: {address.strip()}\nValidated County: {validated_county}\n")

        # Create a unique output file name with the current date and time
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"discrepancies_{timestamp}.txt"

        # Write discrepancies, valid matches, and API errors to the output file
        with open(output_file, 'w') as outfile:
            if discrepancies:
                outfile.write("Discrepancies Found:\n")
                outfile.write("\n\n".join(discrepancies))
                outfile.write("\n\n")

            outfile.write("Valid County Matches:\n")
            outfile.write("\n\n".join(valid_matches))

            if api_errors:
                retry_file = f"retry_401_errors_{timestamp}.txt"
                with open(retry_file, 'w') as retry_outfile:
                    retry_outfile.write("Addresses to Retry (401 Errors):\n")
                    retry_outfile.write("\n\n".join(api_errors))
                print(f"401 errors saved to {retry_file}")

            print(f"Results saved to {output_file}")

    except Exception as e:
        print(f"Error processing addresses: {e}")

if __name__ == "__main__":
    regular_key, credit_key = read_license_key("key.txt")

    if not regular_key:
        print("No valid license key found. Exiting.")
    else:
        FIPS_TO_COUNTY = read_fips_codes("fips.txt")

        if FIPS_TO_COUNTY is None:
            print("Error loading FIPS codes. Exiting.")
        else:
            keys_to_use = [regular_key]
            if credit_key:
                keys_to_use.append(credit_key)
            process_and_compare_addresses("addresses.txt", keys_to_use, FIPS_TO_COUNTY)
