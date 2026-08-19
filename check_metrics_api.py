with open('fastapi_app/main.py', 'r', encoding='utf-8') as f:
    main_py = f.read()

idx = main_py.find('get_project_metrics')
print(main_py[idx:idx+1200].encode('ascii', errors='replace').decode('ascii'))
