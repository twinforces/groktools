# Best Practices for Grok’s Communication with Humans

This document provides guidelines for Grok to communicate effectively with human users, ensuring clarity, efficiency, and adherence to resource constraints in the groktools ecosystem.

## General Guidelines

- **Clarity and Conciseness**: Provide clear, concise responses that directly address the user’s request. Avoid unnecessary verbosity, but ensure all relevant details are included.
- **Fetch Up-to-Date Files**: Always pull the user’s files fresh from the specified location (e.g., GitHub or Google Drive) to ensure you’re working with the latest version. Example: If a user references a file at \`https://github.com/twinforces/groktools/raw/refs/heads/master/examples/apply_patches.sh\`, fetch the raw content directly rather than relying on memory.
- **Acknowledge Constraints**: Be transparent about resource limits (e.g., message size, file size) and suggest workarounds when necessary, such as breaking responses into chunks or using external hosting.

## Handling File Sizes and Resource Limits

- **Complete Files for Small Content**: If a file or response is less than half the resource limit (e.g., message size limit), include the complete content directly in the response. Example: For a small script like \`apply_patches.sh\` with fewer than 100 lines, include the full script.
- **Patches for Medium Content**: If a file exceeds half the resource limit but is still manageable, provide a unified diff patch to modify the file instead of including the full content. Example: For a modified script, generate a \`diff -u\` patch showing the changes.
- **Chunks for Large Content**: If a file or response exceeds the resource limit, break it into chunks and provide each chunk separately, ensuring the user can reassemble them. Example: Split a 1,000-line script into two 500-line chunks and provide instructions for combining them.
- **Use External Hosting for Very Large Files**: For extremely large files (e.g., datasets, binaries), recommend uploading the file to GitHub or Google Drive and provide the raw URL for Grok to fetch. Example: "Please upload your large dataset to Google Drive and share the direct link for me to access."

## Working with grokpatcher

- **Understand grokpatcher Output**: When working with the grokpatcher ecosystem (e.g., \`apply_patches.sh\`, \`grokpatcher.py\`), interpret its output accurately. For example, recognize messages like "Hunk #2 succeeded at 8 with fuzz 2" as successful patch applications with minor context adjustments, and explain any potential issues to the user.
- **Provide grokpatcher-Specific Advice**: Offer suggestions for debugging grokpatcher failures, such as checking the reject file (e.g., \`.rej\`), verifying file paths, and ensuring dependencies like \`diffextract.py\` are present.
- **Automate grokpatcher Workflows**: When generating patches for grokpatcher, follow the guidelines in \`udiff_prompt.md\` to ensure compatibility, and suggest automated workflows (e.g., updating scripts to handle paths dynamically) to prevent common errors.

## File Sharing and Collaboration

- **Use GitHub for Versioned Files**: Prefer GitHub for sharing versioned files, as it allows Grok to fetch the latest version directly from the raw URL (e.g., \`https://raw.githubusercontent.com/twinforces/groktools/master/examples/apply_patches.sh\`). Encourage users to commit changes frequently and provide the exact path or commit hash for clarity.
- **Use Google Drive for Large or Non-Versioned Files**: For large files or non-versioned content (e.g., datasets, logs), recommend Google Drive and ask users to share a direct link (e.g., a "Anyone with the link" URL). Fetch the file content using the provided link to ensure accuracy.
- **Verify File Accessibility**: Before processing a file from GitHub or Google Drive, verify that the link is accessible and the file exists. If a link is broken or inaccessible, inform the user and suggest alternatives (e.g., re-uploading the file or providing a different URL).
- **Automate File Handling**: When working with user files, automate the process of fetching, processing, and returning results. For example, if a user provides a GitHub URL, fetch the file, apply changes, and return a diff or updated file directly in the response.