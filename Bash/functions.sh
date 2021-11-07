remove_prefix() {
    find . -type d -name "$1" -exec sh -c '
        for pathname do
            mv -- "$pathname" "$pathname:"
        done' sh {} +
}