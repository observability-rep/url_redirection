#!/bin/bash

# Function to get the URL redirection
get_url_redirection() {
    local url="$1"
    local enumerate="$2"
    local max_redirections="$3"

    local next_url="$url"
    local urls=("$url")

    if [ "$enumerate" = "true" ]; then
        local ultimate_found=false
        for (( i = 1; i <= max_redirections + 1; i++ )); do
            echo "Examining: $next_url"
            next_url_str=$(curl -s -i -o /dev/null -w "%{redirect_url}" "$next_url")
            echo "Raw target: $next_url_str"

            if [[ ! "$next_url_str" =~ ^https?:// ]]; then
                next_url="http://$next_url_str"
            else
                next_url="$next_url_str"
            fi

            urls+=("$next_url")

            if [ -z "$next_url_str" ]; then
                ultimate_found=true
                break
            fi
        done

        if [ "$ultimate_found" = "false" ]; then
            echo "Enumeration of $url redirections ended before reaching the ultimate target." >&2
        fi

        # Output the array of URLs (chain of redirections) as a *single* object.
        echo "${urls[@]}"
    else
        final_url=$(curl -s -i -o /dev/null -w "%{url_effective}" "$url")
        echo "$final_url"
    fi
}

# Main
input_choice=""
read -p "Input domain name: " input_choice

get_url_redirection "http://$input_choice" true 50