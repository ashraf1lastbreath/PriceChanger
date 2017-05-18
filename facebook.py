import facebook
from facebook import GraphAPI

def main():
  # Fill in the values noted in previous steps here
  cfg = {
    "page_id"      : "1688963914732497",  # Step 1
    "access_token" : "EAAGGAP1HdogBAGQCFHVMVKpzZBD8PkcSZAQc29j3KyfEfzSBq9c24BZBVtS9wjNETW8iMXO5Hc9jQjXEbY84EVhuvZAcZAKdo0CNZCZAHmhBUrwDtNaDmo1PJdxOsC5bBopkyGqIP969LQhrDN5rtWgCMWXu0I30a8ZD"   # Step 3 LONG LIVED
    }

  api = get_api(cfg)
  msg = "Hello, world!"
  status = api.put_wall_post(msg)

def get_api(cfg):
  graph = facebook.GraphAPI(cfg['access_token'])
  # Get page token to post as the page. You can skip 
  # the following if you want to post as yourself. 
  resp = graph.get_object('me/accounts')
  page_access_token = None
  for page in resp['data']:
    if page['id'] == cfg['page_id']:
      page_access_token = page['access_token']
  graph = facebook.GraphAPI(page_access_token)
  return graph
  # You can also skip the above if you get a page token:
  # http://stackoverflow.com/questions/8231877/facebook-access-token-for-pages
  # and make that long-lived token as in Step 3

if __name__ == "__main__":
  main()