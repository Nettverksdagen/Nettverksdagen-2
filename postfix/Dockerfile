FROM juanluisbaptiste/postfix:latest

# Add a delay between every email sent
# Needed to avoid hitting the rate limit
# A bit hacky but it works :)
RUN echo -e "\ndefault_destination_rate_delay = 3s\n" >> /etc/postfix/main.cf 