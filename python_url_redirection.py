import urllib.request

def get_url_redirection(url, enumerate=False, max_redirections=50):
    urls = []
    ultimate_found = False

    if enumerate:
        next_url = url
        urls.append(next_url.geturl())

        for i in range(1, max_redirections + 2):
            print(f"Examining: {next_url}")
            request = urllib.request.Request(next_url, method='HEAD')
            request.add_header('User-Agent', 'Mozilla/5.0')  # Set user agent to avoid 403 error
            request.get_method = lambda: 'HEAD'

            try:
                response = urllib.request.urlopen(request)
                next_url_str = response.getheader('Location')
                response.close()

                if not next_url_str:
                    ultimate_found = True
                    break
            except urllib.error.HTTPError as e:
                next_url_str = e.headers.get('Location', None)

                if not next_url_str:
                    raise
            print(f"Raw target: {next_url_str}")

            if next_url_str.startswith(('http://', 'https://')):
                next_url = prev_url = urllib.parse.urlparse(next_url_str)
            else:
                next_url = prev_url = urllib.parse.urlparse(
                    f"{prev_url.scheme}://{prev_url.netloc}{next_url_str}")

            if i <= max_redirections:
                urls.append(next_url.geturl())

        print(urls)
        if not ultimate_found:
            print(f"Enumeration of {url} redirections ended before reaching the ultimate target.")

    else:
        request = urllib.request.Request(url)
        try:
            response = urllib.request.urlopen(request)
            final_url = response.geturl()
            response.close()
            return final_url
        except urllib.error.HTTPError as e:
            return e.url
        except Exception as e:
            print("An error occurred:", e)

# Example usage:b
# print(get_url_redirection("http://example.com", enumerate=True))
primary_url= input ("Enter url to check (e.g. example.com, do not use spaces). Input url here:")
x = get_url_redirection("https://"+ primary_url)
print (x)