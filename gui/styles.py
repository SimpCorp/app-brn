LIGHT_THEME = """
QWidget {
    background-color: #f5f5f7;
    color: #1d1d1f;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 13px;
}

QFrame#HeaderBar {
    background-color: #ffffff;
    border-bottom: 1px solid #e5e5ea;
}

QLabel#HeaderTitle {
    font-size: 19px;
    font-weight: 600;
    color: #1d1d1f;
}

QLabel#HeaderSubtitle {
    font-size: 12px;
    color: #86868b;
}

QPushButton#SegmentBtn {
    background-color: transparent;
    border: none;
    border-radius: 8px;
    padding: 8px 18px;
    font-weight: 500;
    color: #86868b;
}

QPushButton#SegmentBtn:checked {
    background-color: #ffffff;
    color: #1d1d1f;
    font-weight: 600;
}

QFrame#SegmentContainer {
    background-color: #e5e5ea;
    border-radius: 10px;
}

QTableWidget {
    background-color: #ffffff;
    border: 1px solid #e5e5ea;
    border-radius: 12px;
    gridline-color: #f2f2f7;
    outline: none;
}

QHeaderView::section {
    background-color: #fafafc;
    color: #86868b;
    padding: 10px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    border: none;
    border-bottom: 1px solid #e5e5ea;
}

QPushButton#ActionBtn {
    background-color: #0071e3;
    color: #ffffff;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 600;
    border: none;
}

QPushButton#ActionBtn:hover {
    background-color: #0077ed;
}

QPushButton#ThemeBtn {
    background-color: #ffffff;
    color: #1d1d1f;
    border: 1px solid #d1d1d6;
    border-radius: 8px;
    padding: 6px 14px;
}
"""

DARK_THEME = """
QWidget {
    background-color: #000000;
    color: #f5f5f7;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 13px;
}

QFrame#HeaderBar {
    background-color: #1c1c1e;
    border-bottom: 1px solid #2c2c2e;
}

QLabel#HeaderTitle {
    font-size: 19px;
    font-weight: 600;
    color: #f5f5f7;
}

QLabel#HeaderSubtitle {
    font-size: 12px;
    color: #a1a1a6;
}

QPushButton#SegmentBtn {
    background-color: transparent;
    border: none;
    border-radius: 8px;
    padding: 8px 18px;
    font-weight: 500;
    color: #a1a1a6;
}

QPushButton#SegmentBtn:checked {
    background-color: rgba(255, 255, 255, 0.18);
    color: #ffffff;
    font-weight: 600;
}

QFrame#SegmentContainer {
    background-color: #2c2c2e;
    border-radius: 10px;
}

QTableWidget {
    background-color: #1c1c1e;
    border: 1px solid #2c2c2e;
    border-radius: 12px;
    gridline-color: #2c2c2e;
    outline: none;
}

QHeaderView::section {
    background-color: #242426;
    color: #a1a1a6;
    padding: 10px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    border: none;
    border-bottom: 1px solid #3a3a3c;
}

QPushButton#ActionBtn {
    background-color: #0a84ff;
    color: #ffffff;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 600;
    border: none;
}

QPushButton#ActionBtn:hover {
    background-color: #0071e3;
}

QPushButton#ThemeBtn {
    background-color: #2c2c2e;
    color: #f5f5f7;
    border: 1px solid #3a3a3c;
    border-radius: 8px;
    padding: 6px 14px;
}
"""
