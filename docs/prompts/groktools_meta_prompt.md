# Meta Prompt for Groktools Ecosystem

This prompt provides an overview of the prompts available in the groktools ecosystem, which guide my behavior across various tasks. It ensures I apply the correct guidelines depending on the task at hand.
Base URL: https://github.com/twinforces/groktools/raw/refs/heads/master/

## Available Prompts

- **bestpractices.md**:
  - **Description**: General best practices for me, including DRY principles, concise responses, and collaboration tips.
  - **Location**: \`docs/prompts/bestpractices.md\`

- **changelogs_prompt.md**:
  - **Description**: Guidelines for generating and maintaining changelogs, focusing on version summaries and user-facing updates.
  - **Location**: \`docs/prompts/changelogs_prompt.md\`

- **udiff_prompt.md**:
  - **Description**: Instructions for generating unified diffs compatible with GNU \`patch\`, used in the grokpatcher ecosystem.
  - **Location**: \`docs/prompts/udiff_prompt.md\`

- **grokpatcher_prompt.md**:
  - **Description**: Instructions for working with the grokpatcher ecosystem, including generating and applying \`.grokpatch\` files.
  - **Location**: \`docs/prompts/grokpatcher_prompt.md\`

- **prompt_storage_prompt.md**:
  - **Description**: Instructions for managing prompt storage in the groktools ecosystem, ensuring prompts are organized.
  - **Location**: \`docs/prompts/prompt_storage_prompt.md\`

- **versioning_prompt.md**:
  - **Description**: Guidelines for managing versioning in the groktools ecosystem, using semantic versioning.
  - **Location**: \`docs/prompts/versioning_prompt.md\`

- **human_communications_bestpractices.md**:
  - **Description**: Guidelines for me to communicate effectively with humans, including handling file sizes, resource limits, and file sharing via GitHub or Google Drive.
  - **Location**: \`docs/prompts/human_communications_bestpractices.md\`

## Usage

Refer to the appropriate prompt based on the task. For example, when generating a unified diff, use \`udiff_prompt.md\`. For changelog updates, use \`changelogs_prompt.md\`. 