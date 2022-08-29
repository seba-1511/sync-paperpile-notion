# sync-paperpile-notion

Sync changes in Paperpile to a Notion database.

## Setup

### On Notion

1. Create a new database (e.g. "Papers") with the columns named exactly:

    1. `Title` of type title.
    2. `Authors` of type text.
    3. `Year` of type text.
    4. `Link` of type url.
    5. `Reference ID` of type text.

2. Get the **database identifier** from the database page. If your database url is:

    ```
    https://www.notion.so/my_workspace/aaaabbbbccccddddeeeeffffgggghhhh
    ```

    Then the database identifier is: `aaaabbbbccccddddeeeeffffgggghhhh`.

3. Create a new integration on [https://www.notion.so/my-integrations/](https://www.notion.so/my-integrations/).

    1. Name: Paperpile to Notion
    2. Associated Workspace: Workspace of the database.
    3. Content Capabilities: Read Content, Update Content, Insert Content.
    4. User Capabilities: Read user information, including email addresses.
    5. Press "Submit" and copy the **Internal Integration Token**.

4. On the database page, click "Share" (top right) and add "Paperpile to Notion" with edit access.

### On GitHub

1. Fork this repository with the green "Use this template" button.
2. On you fork, go to: "Settings -> Secrets -> Actions".
3. Create 2 new repository secrets named exactly:
    
    1. `NOTION_TOKEN`: Your integration's internal integration token, from step 3.5 above.
    2. `DATABASE_IDENTIFIER`: Your database identifier, from step 2 above.


### On Paperpile

1. Click on the top-right gear, go to "Workflows and Integrations".
2. Follow the instructions to add a new "BibTex Export", choosing:

    1. Your GitHub repository fork as the repository.
    2. `references.bib` as the export path.

The first sync should start as soon as the Paperpile workflow is created, and subsequent syncs are triggered whenever papers are added or updated in your Paperpile.

**Note**
The first sync might take some time as Notion limits the API rate to ~ 3 requests / second; so if you have 1,000 papers it'll take ~ 6 minutes before they are all available in Notion.
