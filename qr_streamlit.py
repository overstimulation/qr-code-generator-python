import os

import streamlit as st
from PIL import Image

from qr_core import QRCodeGenerator, QRConfig
from translations import t


class QRCodeStreamlit:
    def __init__(self):
        self.generator = QRCodeGenerator()

    def render_language_selector(self):
        """Render compact language selector"""
        language_options = t.get_language_options()

        # Find current language index
        current_index = list(language_options.keys()).index(t.current_language)

        # Compact language selector
        selected_lang = st.selectbox(
            "🌍",
            options=list(language_options.keys()),
            format_func=lambda x: language_options[x],
            index=current_index,
            help=t.get("language.help"),
            label_visibility="collapsed"
        )

        if selected_lang != t.current_language:
            t.set_language(selected_lang)
            st.rerun()

    def render_qr_type_selector(self) -> str:
        """Render a modern QR type selector with compact cards"""
        st.subheader(t.get("qr_types.choose_type"))

        # Define QR types with icons and descriptions from translations
        qr_type_info = {}
        for qr_type in ['text', 'url', 'wifi', 'contact', 'email', 'sms', 'whatsapp', 'phone', 'location', 'event']:
            qr_type_info[qr_type] = {
                'icon': self._get_qr_type_icon(qr_type),
                'title': t.get(f"qr_types.{qr_type}.title"),
                'desc': t.get(f"qr_types.{qr_type}.desc")
            }

        # Create columns for the cards
        cols = st.columns(5)

        # Initialise session state for selected type
        if 'selected_qr_type' not in st.session_state:
            st.session_state.selected_qr_type = 'text'

        # First row
        for i, (qr_type, info) in enumerate(list(qr_type_info.items())[:5]):
            with cols[i]:
                button_style = "primary" if st.session_state.selected_qr_type == qr_type else "secondary"
                if st.button(
                        f"{info['icon']}\n{info['title']} - {info['desc']}",
                        key=f"btn_{qr_type}",
                        use_container_width=True,
                        type=button_style
                ):
                    st.session_state.selected_qr_type = qr_type
                    st.rerun()

        # Second row
        cols2 = st.columns(5)
        for i, (qr_type, info) in enumerate(list(qr_type_info.items())[5:]):
            with cols2[i]:
                button_style = "primary" if st.session_state.selected_qr_type == qr_type else "secondary"
                if st.button(
                        f"{info['icon']}\n{info['title']} - {info['desc']}",
                        key=f"btn_{qr_type}",
                        use_container_width=True,
                        type=button_style
                ):
                    st.session_state.selected_qr_type = qr_type
                    st.rerun()

        return st.session_state.selected_qr_type

    def _get_qr_type_icon(self, qr_type: str) -> str:
        """Get icon for QR type"""
        icons = {
            'text': '📝', 'url': '🌐', 'wifi': '📶', 'contact': '👤', 'email': '📧',
            'sms': '💬', 'whatsapp': '💚', 'phone': '📞', 'location': '📍', 'event': '📅'
        }
        return icons.get(qr_type, '📱')

    def render_data_inputs(self, qr_type: str) -> dict:
        """Render input fields based on QR type"""
        data = {}

        if qr_type == 'text':
            data['text'] = st.text_area(
                t.get("inputs.text.label"),
                help=t.get("inputs.text.help")
            )

        elif qr_type == 'url':
            data['url'] = st.text_input(
                t.get("inputs.url.label"),
                help=t.get("inputs.url.help")
            )

        elif qr_type == 'wifi':
            col1, col2 = st.columns(2)
            with col1:
                data['ssid'] = st.text_input(
                    t.get("inputs.wifi.ssid.label"),
                    help=t.get("inputs.wifi.ssid.help")
                )
                data['password'] = st.text_input(
                    t.get("inputs.wifi.password.label"),
                    type="password",
                    help=t.get("inputs.wifi.password.help")
                )
            with col2:
                data['encryption'] = st.selectbox(
                    t.get("inputs.wifi.encryption.label"),
                    options=['WPA', 'WPA2', 'WEP', 'NONE'],
                    help=t.get("inputs.wifi.encryption.help")
                )

        elif qr_type == 'contact':
            col1, col2 = st.columns(2)
            with col1:
                data['name'] = st.text_input(
                    t.get("inputs.contact.name.label"),
                    help=t.get("inputs.contact.name.help")
                )
                data['email'] = st.text_input(
                    t.get("inputs.contact.email.label"),
                    help=t.get("inputs.contact.email.help")
                )
            with col2:
                data['phone'] = st.text_input(
                    t.get("inputs.contact.phone.label"),
                    help=t.get("inputs.contact.phone.help")
                )
                data['address'] = st.text_area(
                    t.get("inputs.contact.address.label"),
                    help=t.get("inputs.contact.address.help")
                )

        elif qr_type == 'email':
            data['email'] = st.text_input(
                t.get("inputs.email.email.label"),
                help=t.get("inputs.email.email.help")
            )
            col1, col2 = st.columns(2)
            with col1:
                data['subject'] = st.text_input(
                    t.get("inputs.email.subject.label"),
                    help=t.get("inputs.email.subject.help")
                )
            with col2:
                data['body'] = st.text_area(
                    t.get("inputs.email.body.label"),
                    help=t.get("inputs.email.body.help")
                )

        elif qr_type == 'sms':
            col1, col2 = st.columns(2)
            with col1:
                data['phone'] = st.text_input(
                    t.get("inputs.sms.phone.label"),
                    help=t.get("inputs.sms.phone.help")
                )
            with col2:
                data['message'] = st.text_area(
                    t.get("inputs.sms.message.label"),
                    help=t.get("inputs.sms.message.help")
                )

        elif qr_type == 'whatsapp':
            data['phone'] = st.text_input(
                t.get("inputs.whatsapp.phone.label"),
                help=t.get("inputs.whatsapp.phone.help")
            )
            data['message'] = st.text_area(
                t.get("inputs.whatsapp.message.label"),
                help=t.get("inputs.whatsapp.message.help")
            )

        elif qr_type == 'phone':
            data['phone'] = st.text_input(
                t.get("inputs.phone.phone.label"),
                help=t.get("inputs.phone.phone.help")
            )

        elif qr_type == 'location':
            col1, col2 = st.columns(2)
            with col1:
                data['latitude'] = st.text_input(
                    t.get("inputs.location.latitude.label"),
                    help=t.get("inputs.location.latitude.help")
                )
            with col2:
                data['longitude'] = st.text_input(
                    t.get("inputs.location.longitude.label"),
                    help=t.get("inputs.location.longitude.help")
                )

        elif qr_type == 'event':
            data['name'] = st.text_input(
                t.get("inputs.event.name.label"),
                help=t.get("inputs.event.name.help")
            )
            col1, col2 = st.columns(2)
            with col1:
                data['start_date'] = st.text_input(
                    t.get("inputs.event.start_date.label"),
                    help=t.get("inputs.event.start_date.help")
                )
                data['location'] = st.text_input(
                    t.get("inputs.event.location.label"),
                    help=t.get("inputs.event.location.help")
                )
            with col2:
                data['end_date'] = st.text_input(
                    t.get("inputs.event.end_date.label"),
                    help=t.get("inputs.event.end_date.help")
                )
                data['description'] = st.text_area(
                    t.get("inputs.event.description.label"),
                    help=t.get("inputs.event.description.help")
                )

        return data

    def validate_required_fields(self, qr_type: str, data: dict) -> bool:
        """Validate required fields based on QR type"""
        required_fields = {
            'text': ['text'],
            'url': ['url'],
            'wifi': ['ssid'],
            'contact': ['name'],
            'email': ['email'],
            'sms': ['phone'],
            'whatsapp': ['phone', 'message'],
            'phone': ['phone'],
            'location': ['latitude', 'longitude'],
            'event': ['name', 'start_date']
        }

        missing_fields = []
        for field in required_fields.get(qr_type, []):
            if not data.get(field, '').strip():
                missing_fields.append(field)

        if missing_fields:
            st.error(t.get("validation.required_fields", fields=', '.join(missing_fields)))
            return False
        return True

    def render_customisation_options(self) -> dict:
        """Render QR code customisation options"""
        st.subheader(t.get("customisation.title"))

        config = {}

        # Logo upload section
        uploaded_logo = st.file_uploader(
            t.get("customisation.logo.label"),
            type=['png', 'jpg', 'jpeg'],
            help=t.get("customisation.logo.help")
        )

        # Save logo temporarily if uploaded
        logo_path = None
        if uploaded_logo:
            logo_path = f"temp_logo_{uploaded_logo.name}"
            with open(logo_path, "wb") as f:
                f.write(uploaded_logo.getbuffer())

        config['custom_logo'] = logo_path

        # Design options in columns
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**{t.get('customisation.design.title')}**")
            config['fill_color'] = st.color_picker(
                t.get("customisation.design.fill_color.label"),
                value="#000000",
                help=t.get("customisation.design.fill_color.help")
            )
            config['back_color'] = st.color_picker(
                t.get("customisation.design.back_color.label"),
                value="#FFFFFF",
                help=t.get("customisation.design.back_color.help")
            )

        with col2:
            st.markdown(f"**{t.get('customisation.settings.title')}**")
            if logo_path:
                st.info(t.get("customisation.settings.error_correction.logo_info"))
                config['error_correction_level'] = 'H'
            else:
                config['error_correction_level'] = st.selectbox(
                    t.get("customisation.settings.error_correction.label"),
                    options=['L', 'M', 'Q', 'H'],
                    index=0,
                    help=t.get("customisation.settings.error_correction.help")
                )

            config['box_size'] = st.slider(
                t.get("customisation.settings.box_size.label"),
                min_value=1,
                max_value=20,
                value=10,
                help=t.get("customisation.settings.box_size.help")
            )

        # Additional settings in a new row
        col3, col4 = st.columns(2)

        with col3:
            config['border_size'] = st.slider(
                t.get("customisation.settings.border_size.label"),
                min_value=0,
                max_value=10,
                value=4,
                help=t.get("customisation.settings.border_size.help")
            )

        with col4:
            config['filename'] = st.text_input(
                t.get("customisation.filename.label"),
                value="qr_code.png",
                help=t.get("customisation.filename.help")
            )
            if not config['filename'].endswith('.png'):
                config['filename'] += '.png'

        return config

    def run(self):
        """Main Streamlit application"""
        st.set_page_config(
            page_title="QR Code Generator",
            page_icon="📱",
            layout="wide"
        )

        # Custom CSS for better styling and compact card design
        st.markdown("""
        <style>
        .stButton > button {
            height: 60px;
            white-space: normal;
            text-align: center;
            border-radius: 8px;
            border: 2px solid #e0e0e0;
            transition: all 0.3s ease;
            line-height: 1.1;
            padding: 4px 8px;
            font-size: 0.8rem;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        /* Fix language selector styling */
        .stSelectbox > div > div {
            background-color: #f8f9fa;
            border: 1px solid #d0d2d6;
            border-radius: 6px;
        }
        .stSelectbox > div > div > div {
            color: #262730;
            font-weight: 500;
        }
        /* Reduce spacing in button text */
        .stButton > button > div {
            line-height: 1.1 !important;
        }
        /* Improve header layout */
        .main > div {
            padding-top: 1rem;
        }
        </style>
        """, unsafe_allow_html=True)

        # Header with language selector
        header_col1, header_col2, header_col3 = st.columns([1, 2, 1])
        with header_col2:
            st.title(t.get("app.title"))
            st.markdown(f"### {t.get('app.subtitle')}")

        with header_col3:
            # Language selector in header
            self.render_language_selector()

        st.divider()

        # QR type selector
        qr_type = self.render_qr_type_selector()

        st.divider()

        # Get the display name for the selected type
        qr_type_display = t.get(f"qr_types.{qr_type}.title")

        # Two-column layout: Settings on left, Generation on right
        main_col1, main_col2 = st.columns([1.2, 0.8])

        with main_col1:
            # Data inputs section
            st.subheader(t.get("details_title", type=qr_type_display))
            qr_data = self.render_data_inputs(qr_type)

            st.divider()

            # Customisation options
            config_options = self.render_customisation_options()

        with main_col2:
            # Generation section
            st.subheader(t.get("generation.title"))

            # Generate button
            generate_button = st.button(
                t.get("generation.button"),
                type="primary",
                use_container_width=True,
                help=t.get("generation.button_help")
            )

            # Tips section
            with st.expander(t.get("tips.title"), expanded=False):
                st.markdown(f"""
                **{t.get("tips.current_type")}** {qr_type_display}
                
                **{t.get("tips.pro_tips")}**
                """ + "\n".join([f"• {tip}" for tip in t.get_list("tips.pro_tips_content")]) + f"""
                
                **{t.get("tips.design_tips")}**
                """ + "\n".join([f"• {tip}" for tip in t.get_list("tips.design_tips_content")]))

            # QR Code generation and display
            if generate_button:
                if self.validate_required_fields(qr_type, qr_data):
                    with st.spinner(t.get("generation.generating")):
                        try:
                            # Process QR data
                            processed_data = self.generator.process_qr_data(qr_type, qr_data)

                            # Create config
                            config = QRConfig(
                                data_to_encode=processed_data,
                                custom_logo=config_options['custom_logo'],
                                save_path=config_options['filename'],
                                error_correction_level=config_options['error_correction_level'],
                                box_size=config_options['box_size'],
                                border_size=config_options['border_size'],
                                fill_color=config_options['fill_color'],
                                back_color=config_options['back_color']
                            )

                            # Generate QR code
                            if self.generator.generate_qr_code(config):
                                # Display the generated QR code
                                qr_image = Image.open(config_options['filename'])
                                st.image(qr_image, caption=t.get("generation.image_caption"), use_container_width=True)

                                # Download button
                                with open(config_options['filename'], "rb") as file:
                                    st.download_button(
                                        label=t.get("generation.download"),
                                        data=file.read(),
                                        file_name=config_options['filename'],
                                        mime="image/png",
                                        use_container_width=True
                                    )

                                st.success(t.get("generation.success"))

                                # Clean up temp logo file
                                if config_options['custom_logo'] and os.path.exists(config_options['custom_logo']):
                                    os.remove(config_options['custom_logo'])

                                # Clean up QR file after showing
                                if os.path.exists(config_options['filename']):
                                    os.remove(config_options['filename'])

                            else:
                                st.error(t.get("generation.error"))

                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                            # Clean up temp files on error
                            if config_options['custom_logo'] and os.path.exists(config_options['custom_logo']):
                                os.remove(config_options['custom_logo'])


if __name__ == '__main__':
    app = QRCodeStreamlit()
    app.run()
