from pyrobotstxt import RobotsTxt, UserAgent

robots_file = RobotsTxt()

robots_file.include_header("Welcome Crawlers", append_date=True)
robots_file.include_footer("Good Bye Crawlers")

ua_general = UserAgent(ua_name="*")
ua_general.add_allow(
    allow_items=["/home", "/deep", "/home"],
    unique=True,
    comments="This is a list of allowed items",
)

ua_general.add_disallow(
    disallow_items=["/nopi$", "/topi?a", "/img*.png$"],
    unique=True,
    comments="This is a list of allowed items",
)

ua_general_google = UserAgent(ua_name="Google")
ua_general_google.add_allow(
    allow_items=["/home", "/deep", "/home"],
    unique=True,
    comments="This is a list of allowed items",
)
ua_general_google.add_disallow(
    disallow_items=["/nopi$", "/topi?a", "/img*.png$"],
    unique=True,
    comments="This is a list of allowed items",
)
ua_general_google.add_sitemap("https://seowings.org/sitemap.xml")

robots_file.add_user_agent(ua_general)
robots_file.add_user_agent(ua_general_google)

robots_file.write("robots.txt")

# Read Remote File
robots_file_2 = RobotsTxt()
robots_file_2.read("https://nike.com/robots.txt")
robots_file_2.write("nike_robots.txt")

print (robots_file_2.robots_details("Baiduspider"))
