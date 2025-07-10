#!/usr/bin/env python3

from figure import create_partd_figure, df

print("Testing the figure function...")

try:
    fig = create_partd_figure(df)
    print("✓ Figure created successfully!")
    print(f"✓ Figure type: {type(fig)}")
    print(f"✓ Number of traces: {len(list(fig.data))}")
    
    # Test showing the figure (just validate it doesn't crash)
    print("✓ Figure function is working correctly!")
    
    # Optionally save as HTML for testing
    # fig.write_html("test_figure.html")
    # print("✓ Figure saved as test_figure.html")
    
except Exception as e:
    print(f"✗ Error creating figure: {e}")
    import traceback
    traceback.print_exc()
