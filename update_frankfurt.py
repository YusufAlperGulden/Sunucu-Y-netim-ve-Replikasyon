import re

main_path = 'fastapi_app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

OLD_FRANKFURT = "postgresql://neondb_owner:npg_EfQe3IRhHo9K@ep-rapid-star-aszbsk55.c-4.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
NEW_FRANKFURT = "postgresql://neondb_owner:npg_mONv8dTcRuZ2@ep-rapid-star-aszbsk55.c-4.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

if OLD_FRANKFURT in content:
    content = content.replace(OLD_FRANKFURT, NEW_FRANKFURT)
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated Frankfurt URL successfully")
else:
    print("Old Frankfurt URL not found, checking...")
    if NEW_FRANKFURT in content:
        print("New URL already in file")
    else:
        print("Neither URL found!")
