
def imshow(data, text_auto, title):
    """Displays a heatmap.

    Args:
        data: The matrix data.
        text_auto: Whether to display values.
        title: The chart title.

    Returns:
        None.
    """
    if not isinstance(data, list):
        raise TypeError("Data must be a list.")

    for row in data:
        if not isinstance(row, list):
            raise TypeError("Each row in data must be a list.")
        for element in row:
            if not isinstance(element, (int, float)):
                raise TypeError("Each element in data must be a number.")

    if not isinstance(text_auto, bool):
        raise TypeError("text_auto must be a boolean.")

    if not isinstance(title, str):
        raise TypeError("Title must be a string.")

    print(f"Displaying heatmap: {title}")
    for row in data:
        print(row)
