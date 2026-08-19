with open('fastapi_app/main.py', 'r', encoding='utf-8') as f:
    main_py = f.read()

idx = main_py.find('Auto-sync Neon URLs')
print(main_py[idx:idx+1500].encode('ascii', errors='replace').decode('ascii'))
