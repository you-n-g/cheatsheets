
from collections import defaultdict  # Import defaultdict from collections
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient


def main():
    """
    # Please refer to
    # https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/cognitiveservices/azure-mgmt-cognitiveservices/generated_samples/list_deployments.py

    # PREREQUISITES
        pip install azure-identity azure-mgmt-cognitiveservices
    """
    client = CognitiveServicesManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id="e033d461-1923-44a7-872b-78f1d35a86dd",
    )
    res = defaultdict(dict)
    for acc in "MIICSC", "MSRAOpenAIAustraliaEast", "MSRAOpenAICanadaEast", "MSRAOpenAIEastUS", "MSRAOpenAIEastUS2",  "MSRAOpenAINorthCentralUS", "MSRAOpenAISouthCentralUS":
        res[acc]["API_BASE"] = f"https://{acc.lower()}.openai.azure.com/"
        response = client.deployments.list(
            resource_group_name="OpenAI",
            account_name=acc,
        )
        for item in response:
            res[acc].setdefault("deployments", []).append(item.id.split('/')[-1])

    __import__('pprint').pprint(res)


if __name__ == "__main__":
    main()
