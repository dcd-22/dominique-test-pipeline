import requests
import json
import os

api_secret = os.getenv('API_SECRET')

# Set the endpoint URL and headers
url = "https://api.github.com/graphql"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_secret}"
}

# Function to send GraphQL requests
def send_graphql_request(query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = json.dumps(variables)
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
        return None

# Function to extract all IDs from the dictionary
def extract_issue_ids(response_json):
    ids = []
    try:
        # Navigate through the JSON to find items with closed issues
        items = response_json['data']['node']['items']['nodes']
        for item in items:
            content = item.get('content', {})
            if content.get('__typename') == 'Issue' and content.get('state') == 'CLOSED':
                ids.append(item['id'])  # Extracting the node ID for each closed issue
    except KeyError as e:
        print(f"Error extracting IDs: {str(e)}")
    return ids

# Query to fetch issues
issues_id_request = """
    query {
        node(id: "PVT_kwHOByQZQ84AhpCG") { 
            ... on ProjectV2 {
                id
                number
                createdAt
                items(last:100) {
                    nodes {
                        id
                        content {
                            __typename
                            ... on Issue {
                                id
                                number
                                title
                                state
                            }
                        }
                    }
                }
            }
        }
    }
"""

# Send query to fetch issues
response_json = send_graphql_request(issues_id_request)

if response_json:
    # Extracting issue IDs
    issue_ids = extract_issue_ids(response_json)

    print("Extracted Issue IDs:", issue_ids)

    # Mutation to change an issue's status
    mutation = """
    mutation changeStatus($itemId: ID!, $value: ProjectV2FieldValue!) {
        updateProjectV2ItemFieldValue(
            input: {
                fieldId: "PVTSSF_lAHOByQZQ84AhpCGzgaSHPk",  # done field ID
                itemId: $itemId,
                projectId: "PVT_kwHOByQZQ84AhpCG",  # project ID
                value: $value
            }
        ) {
            projectV2Item {
                id
            }
        }
    }
    """

    # Value to be set in mutation
    value = {"singleSelectOptionId": "894df123"}  # Change to the desired value ID

    # Loop through each issue ID and send a mutation request
    for issue_id in issue_ids:
        variables = {
            "itemId": issue_id,
            "value": value
        }
        mutation_response = send_graphql_request(mutation, variables)
        if mutation_response:
            print(f"Mutation successful for issue ID {issue_id}")
        else:
            print(f"Mutation failed for issue ID {issue_id}")

else:
    print("Query failed:", response_json)
