import os
import json
import base64
import re

# Whitelist of allowed departments
allowed_departments = ["operations", "development", "communications"]

def sanitize_input(user_input):
    return re.sub(r"[^\w\s]", "", user_input)

def validate_url(user_input):
    pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:\S+(?::\S*)?@)?'  # optional user:pass authentication
        r'(?:[\w.-]+)'  # domain...
        r'(?:\.[\w\.-]+)*'  # ...with possible subdomains
        r'(?:\.[\w]{2,})'  # last domain extension must be at least 2 characters
        r'(?:[\w\.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'  # path with optional query parameters
    )
    if not pattern.match(user_input):
        print("Invalid URL. Please enter a valid URL.")
        return ""
    return user_input

def read_template_md():
    try:
        with open("template.md", "r") as file:
            return file.read()
    except FileNotFoundError:
        print("Error: The template.md file was not found.")
        return None

def read_markdown_details(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            title = lines[0].replace("# ", "").strip()  # Assuming the first line is the title
            summary_lines = lines[:10]  # Assuming the summary is in the first 10 lines
            summary = " ".join(line.strip() for line in summary_lines).replace("#", "").strip()  # Clean up markdown headers
            details = "".join(lines).strip()  # Entire content as details
        return title, summary, details
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None, None, None

def write_json_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Function to read and parse a JSON file
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
        
def generate_files(department_name, candidate_name, candidate_address, candidate_twitter, candidate_discord, candidate_nomination_url, twitter_space_url, department_contract_addr):
    department_name = department_name.title()  # Capitalize department name
    # Generate Markdown file
    md_template = read_template_md()
    if md_template:
        filled_md = md_template.replace("<Department Name>", department_name) \
                               .replace("<Candidate Name>", candidate_name) \
                               .replace("<Candidate Address>", candidate_address) \
                               .replace("<Candidate Twitter>", candidate_twitter) \
                               .replace("<Candidate Discord>", candidate_discord) \
                               .replace("<Candidate Nomination URL>", candidate_nomination_url) \
                               .replace("<Twitter Space URL>", twitter_space_url)

        # Create directories and save Markdown
        dir_path = os.path.join(department_name.replace(' ', '_').lower(), candidate_name.replace(' ', '_').lower())
        os.makedirs(dir_path, exist_ok=True)
        md_file_path = os.path.join(dir_path, f"{candidate_name.replace(' ', '_').lower()}_proposal.md")
        with open(md_file_path, 'w') as file:
            file.write(filled_md)
        print(f"Markdown file saved at {md_file_path}")

        # Read details for JSON
        proposal_title, proposal_summary, proposal_details = read_markdown_details(md_file_path)

        # Generate proposal.json
        template_json = read_json_file('template.json')
        msg_execute_data = read_json_file('msg_execute_data.json')
        if template_json and msg_execute_data:
            msg_execute_data['update_members']['add'][0]['addr'] = candidate_address
            minified_json = json.dumps(msg_execute_data, separators=(',', ':'))
            base64_msg = base64.b64encode(minified_json.encode()).decode()

            template_json['messages'][0]['contract'] = department_contract_addr
            template_json['messages'][0]['msg'] = base64_msg
            # Update metadata, title, and summary in template_json
            template_json['metadata'] = template_json['metadata'].replace("<Proposal Title>", proposal_title) \
                                                                .replace("<Proposal Summary>", proposal_summary) \
                                                                .replace("<Proposal Details>", proposal_details)
            template_json['title'] = proposal_title
            template_json['summary'] = proposal_summary[:150]  # Assuming we want a shorter summary for this field, adjust as needed

            proposal_json_path = os.path.join(dir_path, "proposal.json")
            write_json_file(proposal_json_path, template_json)
            print(f"JSON proposal saved at {proposal_json_path}")

# Data collection
department_name = input("Enter the Department Name: ")
if department_name.lower() not in allowed_departments:
    print("Department not allowed. Exiting.")
else:
    candidate_name = sanitize_input(input("Enter the Candidate Name: "))
    candidate_address = sanitize_input(input("Enter the Candidate Address: "))
    candidate_twitter = sanitize_input(input("Enter the Candidate Twitter Handle: "))
    candidate_discord = sanitize_input(input("Enter the Candidate Discord Handle: "))
    candidate_nomination_url = validate_url(input("Enter the Candidate Nomination URL: "))
    twitter_space_url = validate_url(input("Enter the Twitter Space URL: "))
    department_contract_addr = sanitize_input(input("Enter the Department Contract Address: "))

    generate_files(department_name, candidate_name, candidate_address, candidate_twitter, candidate_discord, candidate_nomination_url, twitter_space_url, department_contract_addr)
