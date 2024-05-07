package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"
)

func getURLRedirection(url string, enumerate bool, maxRedirections int) string {
	var nextURL string
	var urls []string

	nextURL = url
	urls = append(urls, url)

	client := &http.Client{}
	for i := 1; i <= maxRedirections+1; i++ {
		fmt.Printf("Examining: %s\n", nextURL)

		req, err := http.NewRequest("GET", nextURL, nil)
		if err != nil {
			fmt.Println("Error creating request:", err)
			return ""
		}
		req.Header.Set("User-Agent", "Mozilla/5.0") // Set user agent to avoid 403 error

		resp, err := client.Do(req)
		if err != nil {
			fmt.Println("Error making request:", err)
			return ""
		}
		defer resp.Body.Close()

		// Read response body to discard
		_, err = ioutil.ReadAll(resp.Body)
		if err != nil {
			fmt.Println("Error reading response body:", err)
			return ""
		}

		nextURLStr := resp.Request.URL.String()
		fmt.Printf("Raw target: %s\n", nextURLStr)

		if !strings.HasPrefix(nextURLStr, "http://") && !strings.HasPrefix(nextURLStr, "https://") {
			nextURL = "http://" + nextURLStr
		} else {
			nextURL = nextURLStr
		}

		urls = append(urls, nextURL)

		if resp.StatusCode >= 300 && resp.StatusCode < 400 {
			continue
		}

		break
	}

	fmt.Println(urls)
	return nextURL
}

func main() {
	var inputChoice string
	fmt.Print("Input domain name: ")
	fmt.Scanln(&inputChoice)

	finalURL := getURLRedirection("http://"+inputChoice, true, 50)
	fmt.Println(finalURL)
}
