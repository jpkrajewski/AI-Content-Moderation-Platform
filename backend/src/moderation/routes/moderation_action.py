import http


def list_pending_content():
    """List all pending content that needs moderation"""
    return [
        {
            "id": "content_123",
            "title": "Potentially problematic content",
            "flags": ["inappropriate_language", "hate_speech"],
            "created_at": "2025-04-12T15:30:00Z",
            "user_id": "user_789",
        },
        {
            "id": "content_456",
            "title": "Content under review",
            "flags": ["copyright_violation"],
            "created_at": "2025-04-13T09:45:00Z",
            "user_id": "user_456",
        },
    ], http.HTTPStatus.OK


def get_content_analysis(content_id):
    """Get detailed analysis for specific content"""
    return {
        "id": content_id,
        "title": "Content under review",
        "body": "This is the full text of the content that needs moderation.",
        "analysis": {
            "toxicity_score": 0.82,
            "hate_speech_score": 0.67,
            "copyright_match": 0.12,
            "flags": ["inappropriate_language", "hate_speech"],
            "ai_recommendation": "reject",
        },
        "created_at": "2025-04-12T14:20:00Z",
        "user_id": "user_123",
    }, http.HTTPStatus.OK


def approve_content(content_id):
    """Approve content by ID"""
    return {
        "id": content_id,
        "status": "approved",
        "updated_at": "2025-04-13T12:30:00Z",
        "moderator_id": "admin_456",
    }, http.HTTPStatus.OK


def reject_content(content_id):
    """Reject content by ID"""
    return {
        "id": content_id,
        "status": "rejected",
        "updated_at": "2025-04-13T12:31:00Z",
        "moderator_id": "admin_456",
        "reason": "Violated community guidelines",
    }, http.HTTPStatus.OK


def flag_content(content_id):
    """Flag content for moderation"""
    return {
        "id": content_id,
        "status": "flagged",
        "updated_at": "2025-04-13T12:32:00Z",
        "flag_reason": "Reported by user",
        "reporter_id": "user_789",
    }, http.HTTPStatus.OK
