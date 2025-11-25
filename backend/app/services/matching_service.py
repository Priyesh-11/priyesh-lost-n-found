from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Dict, Any
from app.models.item import Item
from app.schemas.item import ItemOut
from fuzzywuzzy import fuzz

class MatchingService:
    def find_potential_matches(self, db: Session, item: Item) -> List[Dict[str, Any]]:
        """
        Find potential matches for a lost/found item.
        
        Algorithm:
        1. Must match Category (Hard filter)
        2. Must be opposite type (Lost <-> Found)
        3. Score based on:
           - Location match (30%)
           - Title/Description similarity (50%)
           - Date proximity (20%)
        """
        
        # 1. Basic Filtering
        opposite_type = "found" if item.type == "lost" else "lost"
        
        candidates = db.query(Item).filter(
            Item.type == opposite_type,
            Item.category_id == item.category_id,
            Item.status == "active"
        ).all()
        
        matches = []
        
        for candidate in candidates:
            score = 0
            reasons = []
            
            # 2. Location Match (30 points)
            # Exact match or high similarity
            if item.location and candidate.location:
                if item.location.lower() == candidate.location.lower():
                    score += 30
                    reasons.append("Same location")
                elif fuzz.partial_ratio(item.location.lower(), candidate.location.lower()) > 80:
                    score += 20
                    reasons.append("Similar location")
            
            # 3. Text Similarity (50 points)
            # Compare titles and descriptions
            text1 = f"{item.title} {item.description}".lower()
            text2 = f"{candidate.title} {candidate.description}".lower()
            
            text_score = fuzz.token_set_ratio(text1, text2)
            
            if text_score > 80:
                score += 50
                reasons.append("High text similarity")
            elif text_score > 60:
                score += 30
                reasons.append("Moderate text similarity")
            elif text_score > 40:
                score += 10
            
            # 4. Date Proximity (20 points)
            # If lost date is close to found date
            date1 = item.date_lost or item.date_found or item.created_at
            date2 = candidate.date_lost or candidate.date_found or candidate.created_at
            
            if date1 and date2:
                diff_days = abs((date1 - date2).days)
                if diff_days <= 1:
                    score += 20
                    reasons.append("Same day")
                elif diff_days <= 3:
                    score += 15
                    reasons.append("Within 3 days")
                elif diff_days <= 7:
                    score += 10
                    reasons.append("Within a week")
            
            # Threshold for considering it a match
            if score >= 40:
                matches.append({
                    "item": candidate,
                    "score": score,
                    "reasons": reasons
                })
        
        # Sort by score descending
        matches.sort(key=lambda x: x["score"], reverse=True)
        
        return matches

matching_service = MatchingService()
