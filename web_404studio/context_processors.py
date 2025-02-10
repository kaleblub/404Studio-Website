def meeting_links_context(request):
    return {
        "meeting_links": {
            "dev_basic": "https://cal.com/404-studio-kaleb-humpal/meeting-to-discuss-web-development-package-basic",
            "dev_standard": "https://cal.com/404-studio-kaleb-humpal/meeting-to-discuss-web-development-package-standard",
            "dev_premium": "https://cal.com/404-studio-kaleb-humpal/meeting-to-discuss-web-development-package-premium",
            "host_basic": "https://cal.com/404-studio-kaleb-humpal/meeting-to-discuss-hosting-plan-basic",
            "host_standard": "https://cal.com/404-studio-kaleb-humpal/meeting-to-discuss-hosting-plan-standard",
            "host_premium": "https://calendly.com/kaleblub/meeting-to-discuss-hosting-plan-premium",
        }
    }
