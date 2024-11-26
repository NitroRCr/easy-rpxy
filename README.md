# easy-rpxy
 Simple reverse proxy for frontend CORS

## Frontend usage

```javascript
const baseURL = ''

export async function corsFetch(url, { method = 'GET', headers = {}, body }) {
  const response = await fetch(`${baseURL}/proxy`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      method,
      url,
      headers,
      body
    })
  })
  return response
}
```
