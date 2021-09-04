npm create-react-app "$1"
rm -r "$1"/src/*
touch "$1"/src/index.css
first_lines="
import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
"
echo "$first_lines" >> "$1"/src/index.js