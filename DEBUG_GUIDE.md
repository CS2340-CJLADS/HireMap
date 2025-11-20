# Debug & Verification Guide

## 🐛 Fixes Applied

### Issue 1: Current Location Button Not Working ✅
**Problem**: Event listeners were inside conditional block
**Fix**: Moved current location event listeners outside the `{% if user_location %}` block so they work regardless of saved address

### Issue 2: No Circles Showing ✅
**Problem**: Circle drawing functions had incorrect conditions
**Fix**: 
- `updateCommuteCircle()` now always draws teal circle when user has home address
- `updateCurrentLocationCircle()` now always draws red circle when current location is active
- Both circles can be visible simultaneously

### Issue 3: Home Circle Disappearing ✅
**Problem**: getCurrentLocation() was hiding the home circle
**Fix**: Removed code that hid home circle - both should be visible together

### Issue 4: updateMapMarkers() Logic ✅
**Problem**: Function wasn't properly checking both radii
**Fix**: Now uses OR logic - shows jobs within EITHER home radius OR current location radius

---

## 🧪 Testing Steps

### Test 1: Verify Button Works (No Saved Address)
1. Log in as applicant WITHOUT setting address in profile
2. Go to seeker dashboard
3. Click "Map View"
4. You should see ONLY the Current Location card (no Home card)
5. Click "Use Current Location" button
6. Allow browser permission
7. **Expected**: Red marker + red circle appear on map

### Test 2: Verify Home Radius (With Saved Address)
1. Edit your profile and add a valid address
2. Go to seeker dashboard
3. Click "Map View"  
4. **Expected**: You should see TWO cards:
   - Left: 🏠 Home Address Radius with teal slider
   - Right: 📍 Current Location with red button
5. Move the home slider
6. **Expected**: Teal circle grows/shrinks on map

### Test 3: Verify Current Location (With Saved Address)
1. With both cards visible
2. Click "Use Current Location"
3. Allow permission
4. **Expected**:
   - Red marker appears at your location
   - Red circle appears
   - **TEAL CIRCLE STILL VISIBLE** (both at same time)
   - Slider appears below button
   - Move current location slider
   - Red circle grows/shrinks

### Test 4: Verify Dual Radius Logic
1. With both circles visible
2. Create test job postings at different locations:
   - Job A: Within home radius only
   - Job B: Within current radius only  
   - Job C: Within both radii
   - Job D: Outside both radii
3. **Expected**:
   - Jobs A, B, C visible (OR logic)
   - Job D not visible
   - Remote jobs always visible

---

## 🔍 Browser Console Checks

### Open Console (F12)

#### Check 1: Verify Variables Exist
```javascript
// After clicking Map View, check:
typeof map !== 'undefined'  // Should be true
typeof updateMapMarkers !== 'undefined'  // Should be true
typeof getCurrentLocation !== 'undefined'  // Should be true
```

#### Check 2: Verify Event Listener Attached
```javascript
// After map loads, check:
document.getElementById('get-current-location-btn')  // Should not be null
```

#### Check 3: Test Functions Manually
```javascript
// After clicking "Use Current Location":
currentLocationLat  // Should show your latitude
currentLocationLon  // Should show your longitude
isUsingCurrentLocation  // Should be true
```

#### Check 4: Verify Circles
```javascript
// With home address:
commuteCircle  // Should be an object, not null

// After using current location:
currentLocationCircle  // Should be an object, not null

// Both should exist at the same time
```

---

## ⚠️ Common Issues & Solutions

### Issue: Button exists but nothing happens when clicked

**Check**:
```javascript
// In console:
document.getElementById('get-current-location-btn').onclick
// Should show: ƒ getCurrentLocation()
```

**If null**: Clear cache and hard refresh (Ctrl+Shift+R)

---

### Issue: No permission dialog appears

**Check**: 
- Are you on HTTPS or localhost? (Required for geolocation)
- Did you previously deny permission? Check browser settings

**Fix**: 
1. Chrome: Click lock icon in address bar → Site Settings → Location → Allow
2. Firefox: Click (i) icon → Permissions → Location → Allow

---

### Issue: Home card not showing

**Check**:
```javascript
// In console, check template context:
'{{ template_data.user_has_address }}'  // Should be 'True'
'{{ template_data.user_location.lat }}'  // Should show number
```

**If False**: 
1. Edit profile
2. Enter full address (use autocomplete if you added API key)
3. Save
4. Refresh dashboard

---

### Issue: Circles not drawing

**Check Console for Errors**:
- Look for JavaScript errors
- Check if Leaflet is loaded: `typeof L !== 'undefined'`

**Verify Circle Functions**:
```javascript
// After map loads with home address:
updateCommuteCircle(50);  // Should draw teal circle

// After getting current location:
updateCurrentLocationCircle(25);  // Should draw red circle
```

---

### Issue: Sliders not changing circle size

**Test**:
```javascript
// After map loads:
const slider = document.getElementById('map-commute-radius');
slider.value = 75;  // Change value
slider.dispatchEvent(new Event('input'));  // Trigger event
// Teal circle should resize
```

---

### Issue: Jobs not filtering

**Check**:
```javascript
// After map loads:
allJobs.length  // Should show number of jobs
jobMarkers.length  // Should show number of visible markers

// After changing radius:
// jobMarkers.length should update
```

---

## ✅ Success Checklist

After fixes, you should see:

### Visual Elements
- [x] Two white cards with gradient background container
- [x] Teal house icon on left card
- [x] Red pin icon on right card
- [x] Font Awesome icons render (not boxes)
- [x] Sliders have colored thumbs (teal and red)

### Functionality  
- [x] "Use Current Location" button clickable
- [x] Browser asks for location permission
- [x] Red marker appears on map
- [x] Red circle appears on map
- [x] Teal circle ALSO visible (both at once)
- [x] Moving sliders resizes circles
- [x] Job markers update when circles change
- [x] "Clear" button removes current location

### Map Display
- [x] Blue home marker (if address saved)
- [x] Teal circle around home (if address saved)
- [x] Red current location marker (when active)
- [x] Red circle around current (when active)
- [x] Both circles visible simultaneously
- [x] Circles semi-transparent (15% opacity)

---

## 🎯 Expected Behavior Summary

### Without Saved Address
- Only see Current Location card
- Click button → get current location
- Red marker + red circle appear
- Jobs within red circle shown

### With Saved Address
- See both Home and Current Location cards
- Home slider works immediately (teal circle)
- Click current location button
- Both circles appear (teal AND red)
- Jobs in EITHER circle shown (OR logic)

### Dual Radius Active
```
Home Circle (Teal):     ●━━━━━━━━━━━━━━━━●
                         ↓ Jobs here shown ↓

Current Circle (Red):          ●━━━━━━━━●
                                ↓ Jobs here shown ↓

Overlap:                    ●━━━━●━━━●
                             ↓ Definitely shown ↓

Outside Both:     ●                          ●
                   ↓ Not shown (unless remote) ↓
```

---

## 🔧 If Still Not Working

1. **Check Django is running**: `python manage.py runserver`
2. **Clear ALL cache**: Browser cache + Django cache
3. **Hard refresh**: Ctrl+Shift+F5 (Windows) or Cmd+Shift+R (Mac)
4. **Check Network tab**: Any 404s loading scripts?
5. **Try incognito**: Rules out extension conflicts
6. **Check console**: Any red error messages?

---

## 📞 Quick Diagnostics

Run this in console after loading map:
```javascript
console.log({
  mapExists: typeof map !== 'undefined',
  hasHomeLocation: typeof userLat !== 'undefined',
  hasCurrentLocation: currentLocationLat !== null,
  homeCircleExists: typeof commuteCircle !== 'undefined' && commuteCircle !== null,
  currentCircleExists: typeof currentLocationCircle !== 'undefined' && currentLocationCircle !== null,
  markersCount: jobMarkers ? jobMarkers.length : 0,
  totalJobs: allJobs ? allJobs.length : 0,
  buttonExists: document.getElementById('get-current-location-btn') !== null,
  hasEventListener: !!document.getElementById('get-current-location-btn')?.onclick
});
```

This will show you exactly what's working and what's not.

---

**All fixes are now in place! The dual-radius system should be fully functional.** 🎉

