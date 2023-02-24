export const truncateString = (text) => {
    const max_length = 60;

    if (text.length > max_length) {
        let lasSpaceIndex = text.lastIndexOf(' ',max_length)
        text = text.slice(0, lasSpaceIndex) + '...';
    } 
    return text
}

