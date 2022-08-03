def get_max_bid(listing):
    """gets the highest bid price for a listing"""
    listing_bids = listing.bids.all()
    if listing_bids:
        listing.max_bid = max([bid.bid_price for bid in listing_bids])
        return listing.max_bid


def get_max_user_bid(user, listing):
    """gets the user's highest bid for a listing"""
    user_bids = [bid for bid in listing.bids.all() if bid.bidder == user]
    if user_bids:
        return max([bid.bid_price for bid in user_bids])


def highest_bid(user, listing):
    """check if user has the highest bid for a listing"""
    max_bid = get_max_bid(listing)
    if max_bid != None:
        return max_bid == get_max_user_bid(user, listing)
