# Address Editing Fix - Summary

## ✅ ISSUE RESOLVED: Profile Address Editing Now Works

### Problem
When trying to edit your address in the profile, the Google Places autocomplete was preventing manual entry of address fields.

### Root Cause
1. Google Places API script was loading with `YOUR_API_KEY` (invalid)
2. Script was failing to load but blocking manual input
3. No fallback mechanism for manual address entry

### Solution Implemented

#### 1. **Made Autocomplete Optional** ✅
- Modified `initAutocomplete()` to gracefully handle missing/invalid API
- Added error handling so manual entry works even if Google Maps fails
- Script now fails silently if API key is invalid

#### 2. **Added Server-Side Geocoding Fallback** ✅
- When you manually enter an address (without autocomplete):
  - View checks if lat/lon coordinates were provided
  - If not, it automatically geocodes your address using Nominatim
  - Coordinates are saved for map filtering

#### 3. **Preserved Existing Coordinates** ✅
- Hidden lat/lon fields now pre-populate with saved values
- You can edit address without losing map functionality

---

## How It Works Now

### With Google API Key (Optional)
1. Type in street address field
2. See dropdown suggestions from Google Places
3. Select an address → all fields auto-fill
4. Coordinates automatically saved

### Without API Key (Manual Entry - NOW WORKS!)
1. Type in street address field
2. No dropdown appears (API not configured)
3. **You can still type freely** ✅
4. Fill in city, state, zip manually
5. Click "Save Changes"
6. **Server automatically geocodes your address** ✅
7. Coordinates saved for map filtering

---

## What Changed

### Files Modified:

#### 1. `accounts/templates/accounts/profile_edit.html`
**Changes:**
- Added error handling to `initAutocomplete()`
- Made it check if Google Maps API is available
- Added `onerror` handler to script tag
- Pre-populate hidden lat/lon fields with existing values
- Added helpful comments about manual entry

**Key Code:**
```javascript
function initAutocomplete() {
    // Check if Google Maps API is available
    if (typeof google === 'undefined' || typeof google.maps === 'undefined') {
        console.log('Google Maps API not loaded - manual entry still works');
        return; // Exit gracefully, allow manual entry
    }
    
    // ... rest of autocomplete code ...
}
```

#### 2. `accounts/views.py` - `profile_edit()`
**Changes:**
- Added geocoding fallback for manual address entry
- Validates lat/lon before saving
- Calls `geocode_address()` when coordinates not provided
- Handles invalid coordinate values gracefully

**Key Code:**
```python
lat = request.POST.get('lat', '').strip()
lon = request.POST.get('lon', '').strip()

if lat and lon:
    # Use coordinates from autocomplete
    try:
        applicant.location_lat = float(lat)
        applicant.location_lon = float(lon)
    except (ValueError, TypeError):
        lat = lon = None

# Fallback: geocode the address if no coordinates
if not (lat and lon) and (applicant.street_address or applicant.city):
    geocode_result = geocode_address(
        post_code=applicant.post_code,
        street_address=applicant.street_address,
        city=applicant.city,
        state=applicant.state,
        country=applicant.country
    )
    if geocode_result:
        applicant.location_lat = geocode_result['lat']
        applicant.location_lon = geocode_result['lon']
```

---

## Testing Instructions

### Test 1: Manual Entry (No API Key)
1. Go to your profile edit page
2. Click in "Street Address" field
3. **Verify you can type freely** ✅
4. Enter your address manually:
   - Street Address: `123 Main St`
   - City: `Atlanta`
   - State: `GA`
   - Post Code: `30303`
5. Click "Save Changes"
6. **Address should save successfully** ✅
7. Go to job seeker dashboard → Map View
8. **Teal circle should appear around your location** ✅

### Test 2: With Google API Key (If Configured)
1. Replace `YOUR_API_KEY` with actual Google Places API key
2. Go to profile edit page
3. Start typing in street address
4. **See dropdown suggestions** ✅
5. Select an address
6. **All fields auto-fill** ✅
7. Save and verify map shows teal circle

### Test 3: Edit Existing Address
1. With a saved address
2. Go to profile edit
3. Change street address manually
4. Change city manually
5. **Fields should be editable** ✅
6. Save changes
7. **New address saved with new coordinates** ✅

---

## Geocoding Service

### How Automatic Geocoding Works
When you manually enter an address without autocomplete:

1. **You enter:**
   - Street: 123 Main St
   - City: Atlanta
   - State: GA
   - Zip: 30303

2. **Server sends to Nominatim:**
   - Query: "123 Main St, Atlanta, GA 30303, USA"

3. **Nominatim returns:**
   - Latitude: 33.7490
   - Longitude: -84.3880

4. **Saved to database:**
   - `location_lat = 33.7490`
   - `location_lon = -84.3880`

5. **Map uses coordinates:**
   - Draws teal circle at (33.7490, -84.3880)
   - Filters jobs by distance from that point

### Fallback Chain
```
1. Use autocomplete coordinates (if Google API works)
   ↓ (if failed or not used)
2. Use manually entered lat/lon (if provided in hidden fields)
   ↓ (if not provided)
3. Geocode the address using Nominatim (server-side)
   ↓ (if that fails)
4. Save address without coordinates (no map filtering)
```

---

## Common Scenarios

### Scenario 1: First Time User
- **Before**: Couldn't enter address (blocked)
- **Now**: Can type freely, gets geocoded automatically ✅

### Scenario 2: Existing User Editing Address
- **Before**: Fields blocked, couldn't edit
- **Now**: Can edit any field, coordinates update ✅

### Scenario 3: Invalid Google API Key
- **Before**: Script error, fields blocked
- **Now**: Script fails silently, manual entry works ✅

### Scenario 4: No Internet (Geocoding Fails)
- **Before**: Would fail completely
- **Now**: Address saves, just no map filtering (graceful degradation) ✅

---

## Benefits

1. **✅ Always Works**: Manual entry as fallback
2. **✅ Better UX**: Autocomplete when available, manual when not
3. **✅ Flexible**: Works with or without Google API key
4. **✅ Robust**: Multiple geocoding methods
5. **✅ User-Friendly**: Can edit addresses anytime

---

## For Developers

### To Enable Google Places Autocomplete:
1. Get Google Places API key from [Google Cloud Console](https://console.cloud.google.com/)
2. Enable "Places API" and "Maps JavaScript API"
3. In `accounts/templates/accounts/profile_edit.html`, replace:
   ```html
   <script src="...?key=YOUR_API_KEY&...">
   ```
   With:
   ```html
   <script src="...?key=YOUR_ACTUAL_API_KEY&...">
   ```
4. Same for `accounts/templates/accounts/recruiter_profile_edit.html`

### Geocoding Service Used:
- **Service**: Nominatim (OpenStreetMap)
- **Endpoint**: `https://nominatim.openstreetmap.org/search`
- **Rate Limit**: 1 request/second (handled by function)
- **Free**: Yes, no API key required
- **Accuracy**: Good for most addresses

---

## Summary

**You can now freely edit your address!** The profile edit page works in three modes:

1. **Best**: Google Places autocomplete (with API key)
2. **Good**: Manual entry + server geocoding (no API key needed)
3. **Fallback**: Manual entry only (if geocoding fails)

All three modes save your address successfully. The map will show the teal circle as long as geocoding works (which it should for most valid addresses).

**Try it now:**
1. Go to your profile
2. Click "Edit Profile"
3. Update your address
4. Save
5. Check the map view for the teal home radius circle!

---

Last Updated: November 20, 2025

