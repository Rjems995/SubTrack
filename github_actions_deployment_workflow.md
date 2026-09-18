# STREAMING_CHUNK:Defining workflow name and trigger events...
name: Deploy SubTrack to GitHub Pages

on:
  push:
    branches: [ "main" ]

# STREAMING_CHUNK:Setting workflow permissions for GitHub Pages...
permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: true

# STREAMING_CHUNK:Configuring deployment jobs and steps...
jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Setup Pages
        uses: actions/configure-pages@v3

      - name: Upload Artifacts
        uses: actions/upload-pages-artifact@v2
        with:
          path: '.'

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v2