# Juno Network Elections

This repository includes proposals for Juno Charter Elections and utils scripts.

##  Proposal generator script

The Proposal Generator Script streamlines the process of generating structured proposals for department elections, accommodating both "execute" and "text" proposal types. This script facilitates the creation of Markdown and JSON files tailored to each candidate's nomination, adhering to predefined templates.

## Features

- **Proposal Type Selection**: Supports both "execute" and "text" proposals, utilizing respective Markdown templates and adjusting the JSON output accordingly.
- **Input Validation**: Incorporates validation for URLs and sanitizes other inputs to prevent the inclusion of unwanted characters.
- **Markdown Generation**: Automatically generates a Markdown file with the nominee's details based on the selected proposal type.
- **JSON Proposal Creation**: Produces a `proposal.json` file, encoding specific details in base64 for "execute" proposals and adjusting content for "text" proposals.

## Prerequisites

Ensure Python 3.6 or later is installed on your system to run the script. Additionally, prepare the following template files in the script's directory:

- `template_with_execute.md` for "execute" proposals
- `template_without_execute.md` for "text" proposals

## How to Use

1. **Run the Script**: Navigate to the script's directory in your terminal and execute:

   ```bash
   python generate.py
   ```

2. **Follow Prompts**: Enter the required information as prompted:

   - Proposal Type (`execute` or `text`)
   - Department Name (limited to whitelisted departments)
   - Candidate Name, Address, Twitter Handle, Discord Handle
   - Candidate Nomination URL, Twitter Space URL
   - Department Contract Address (for "execute" proposals)

3. **Generated Files**: The script produces:
   - A Markdown file within a structured directory (`/department_name/candidate_name/candidate_name_proposal.md`).
   - A `proposal.json` file in the same directory, tailored to the proposal type.

## Broadcasting the Transaction

For "execute" proposals requiring submission to a blockchain, use the `junod` CLI with Cosmos-SDK v0.47 specifications:

1. **Prepare the Transaction**:

   ```bash
   junod tx gov submit-proposal --from <YourWalletName> --chain-id <ChainID> --proposal "proposal.json" --deposit <DepositAmount>ujuno -y
   ```

   Replace placeholders with your wallet name, chain ID, and deposit amount.

2. **Broadcast the Transaction**:
   Broadcast the signed transaction to the network. Check the transaction status using:

   ```bash
   junod query tx <TxHash>
   ```

## Customization

Adjust `template_with_execute.md`, `template_without_execute.md`, and the whitelisted departments in the script as needed to fit your specific proposal requirements.

## Troubleshooting

- **Invalid URLs**: Ensure URLs begin with `http://` or `https://` and are correctly formatted.
- **Permission Issues**: Verify write permissions in the script's directory to allow file and directory creation.

For additional assistance or to report issues, please open an issue on the project's GitHub repository.

## Contract Addresses

- **Operations**: `juno14dmlcpszxrqx6dhcavmwep2nh2dam9fs9whzgmdeluqxzng9vx2qpr2vx6`
- **Developement**: `juno10uy49jku989yj2f4dmj4yplqsrjy9vedwrjflakwkvtalwu0nlusadmcz0`
