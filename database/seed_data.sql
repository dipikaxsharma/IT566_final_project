USE dipika_ad_project;

INSERT INTO campaign (name, company, budget, status, start_date, end_date) VALUES
('Fall Enrollment Push', 'Marymount University', 5000.00, 'active', '2026-08-01', '2026-09-15'),
('Summer Clearance', 'Northside Retail', 2000.00, 'ended', '2026-06-01', '2026-06-30'),
('Brand Awareness Q3', 'Northside Retail', 8000.00, 'active', '2026-07-01', NULL);

INSERT INTO channel (name, type, status) VALUES
('Instagram Ads', 'social', 'active'),
('Weekly Email Newsletter', 'email', 'active'),
('Google Search Ads', 'search', 'active'),
('YouTube Pre-roll', 'video', 'inactive');

INSERT INTO campaign_channel_xref (campaign_id, channel_id, spend, start_date) VALUES
(1, 1, 2000.00, '2026-08-01'),
(1, 3, 3000.00, '2026-08-05'),
(2, 4, 2000.00, '2026-06-01'),
(3, 1, 4000.00, '2026-07-01'),
(3, 2, 4000.00, '2026-07-01');
