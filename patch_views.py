"""Patch store/views.py to add moments to package_detail_view context."""
content = open('store/views.py', 'r', encoding='utf-8').read()

# Normalize to LF for matching
normalized = content.replace('\r\n', '\n')

old = """    \n    context = {
        'package': package,
        'related_packages': related_packages,
        'gallery': gallery,
        'flights': flights,
    }
    
    return render(request, 'store/package_detail.html', context)"""

new = """    from store.moments_data import get_moments
    moments = get_moments(package.destination.name)

    context = {
        'package': package,
        'related_packages': related_packages,
        'gallery': gallery,
        'flights': flights,
        'moments': moments,
    }
    
    return render(request, 'store/package_detail.html', context)"""

if old in normalized:
    patched = normalized.replace(old, new, 1)
    open('store/views.py', 'w', encoding='utf-8', newline='\n').write(patched)
    print('SUCCESS: moments added to context')
else:
    # Find and show what's actually there
    idx = normalized.find("'package': package")
    print('BLOCK NOT MATCHED. Showing actual content:')
    print(repr(normalized[idx-30:idx+250]))
