#!/bin/bash

export SSL=true
export OCTOKIT_API_ENDPOINT=https://git.corp.adobe.com/api/v3
export OCTOKIT_WEB_ENDPOINT=https://git.corp.adobe.com/
export PAGES_PAGES_HOSTNAME=https://git.corp.adobe.com/pages
bundle exec jekyll serve -lw

