CREATE DATABASE IF NOT EXISTS dipika_ad_project;
USE dipika_ad_project;
CREATE TABLE campaign (
    campaign_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    company VARCHAR(100) NOT NULL,
    budget DECIMAL(10,2),
    status ENUM('active', 'paused', 'ended'),
    start_date DATE,
    end_date DATE
);

CREATE TABLE channel (
    channel_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type ENUM('social', 'search', 'email', 'video'),
    status ENUM('active', 'inactive')
);

CREATE TABLE campaign_channel_xref (
    xref_id INT AUTO_INCREMENT PRIMARY KEY,
    campaign_id INT,
    channel_id INT,
    spend DECIMAL(10,2),
    start_date DATE,
    FOREIGN KEY (campaign_id) REFERENCES campaign(campaign_id),
    FOREIGN KEY (channel_id) REFERENCES channel(channel_id)
);
