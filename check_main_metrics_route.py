with open('fastapi_app/main.py', 'r', encoding='utf-8') as f:
    main_py = f.read()

idx = main_py.find('/metrics')
print(main_py[idx-100:idx+1500].encode('ascii', errors='replace').decode('ascii'))
