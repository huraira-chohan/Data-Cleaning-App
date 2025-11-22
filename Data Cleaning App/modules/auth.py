import streamlit as st
import hashlib
from .logger import get_logger

logger = get_logger('auth')


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def login_form():
    """Render a simple login form in the sidebar.
    Behavior:
    - If `.streamlit/secrets.toml` has an `[auth]` section with `username` and `password_hash` (or `password`), use it.
    - If no auth is configured, show a helpful notice and offer a "Continue (dev)" button to bypass locally.
    Returns True when logged in.
    """
    st.sidebar.header("🔐 Login")
    # If user already logged in, short-circuit
    if st.session_state.get('logged_in'):
        return True

    # Read secrets safely: avoid calling `st.secrets` if no secrets.toml exists
    secrets = {}
    try:
        # Check common locations for a secrets.toml before asking Streamlit
        from pathlib import Path
        import os

        cwd = Path.cwd()
        possible = [Path.home() / '.streamlit' / 'secrets.toml', cwd / '.streamlit' / 'secrets.toml']
        secrets_file_exists = any(p.exists() for p in possible)
        if secrets_file_exists and hasattr(st, 'secrets'):
            try:
                secrets = st.secrets.get('auth', {})
            except Exception as e:
                logger.info(f"Could not parse secrets via st.secrets: {e}")
        else:
            logger.info("No secrets.toml found; running in dev-mode for auth helper")
            secrets = {}
    except Exception as e:
        logger.info(f"Unexpected error while checking secrets files: {e}")

    expected_user = secrets.get('username')
    expected_pw_hash = secrets.get('password_hash') or secrets.get('password')

    if expected_user is None or expected_pw_hash is None:
        st.sidebar.warning("Authentication is not configured. To secure the app, add credentials to `.streamlit/secrets.toml`.")
        st.sidebar.markdown("Use the helper below to generate a sha256 `password_hash` for `.streamlit/secrets.toml` during development.")
        # Helper to generate a sha256 password hash locally
        with st.sidebar.expander("Password hash helper (dev)"):
            gen_pw = st.text_input("Enter plain password to hash", key="gen_pw")
            if st.button("Generate hash") and gen_pw:
                st.code(hash_password(gen_pw))
                st.sidebar.success("Copy this hash into `.streamlit/secrets.toml` under `[auth] -> password_hash`")
        if st.sidebar.button("Continue (dev)"):
            st.session_state['logged_in'] = True
            logger.info("Dev bypass login used")
            return True
        return False

    # Render login fields
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Log in"):
        try:
            provided_hash = hash_password(password)
            # If stored value looks like a sha256 hex, compare directly; else compare its hash
            stored = expected_pw_hash
            if stored is None:
                st.sidebar.error("Authentication configuration seems incomplete.")
                return False
            stored_str = str(stored)
            if len(stored_str) == 64 and all(c in '0123456789abcdef' for c in stored_str.lower()):
                match = provided_hash == stored_str.lower()
            else:
                # stored may be plain password
                match = password == stored_str

            if username == expected_user and match:
                st.session_state['logged_in'] = True
                logger.info(f"User '{username}' logged in")
                return True
            else:
                st.sidebar.error("Invalid credentials — check username/password or your `.streamlit/secrets.toml` entry.")
                return False
        except Exception as e:
            logger.exception(f"Error during login: {e}")
            st.sidebar.error(f"Authentication error: {e}")
            return False

    return False
