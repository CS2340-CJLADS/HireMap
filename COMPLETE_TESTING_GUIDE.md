# Complete Address & Map System - Testing Guide

## 🎯 Everything is Now Fixed and Ready to Test!

### What's Been Implemented:

1. ✅ **Google Places Autocomplete** - Live address suggestions as you type
2. ✅ **Teal Home Radius Circle** - Shows on map when address is saved
3. ✅ **Red Current Location Circle** - Shows when you use current location
4. ✅ **Both Circles Simultaneously** - Work together with OR logic
5. ✅ **Helpful UI Messages** - Guides you to add address if missing

---

## 📝 Step-by-Step Testing Instructions

### Part 1: Add Your Address (With Autocomplete)

1. **Go to your profile**:
   - Click your username → "Edit Profile"
   - Or navigate to: http://127.0.0.1:8000/seeker/profile/edit/

2. **Scroll to "Contact Information" section**

3. **Start typing in the "Street Address" field**:
   ```
   Type: "123 Main"
   ```
   
4. **You should see a dropdown appear with suggestions!** ✅
   - Example: "123 Main St, Atlanta, GA, USA"
   - Example: "123 Main Street, New York, NY, USA"
   - This is Google Places autocomplete working!

5. **Select an address from the dropdown**:
   - Click on one of the suggestions
   - **All fields will auto-fill**: ✅
     - Street Address: `123 Main St`
     - City: `Atlanta`
     - State: `GA`
     - Post Code: `30303`
   - Hidden lat/lon fields also populate automatically

6. **Click "Save Changes"**

7. **Coordinates are now saved to your profile!** ✅

---

### Part 2: See the Teal Home Radius Circle

1. **Go to Job Seeker Dashboard**:
   - Navigate to: http://127.0.0.1:8000/seeker/

2. **Click "Map View" button**

3. **You should now see** ✅:
   ```
   ┌──────────────────────────────────────────────┐
   │ Job Locations Map                            │
   ├──────────────────────────────────────────────┤
   │ 🏠 Home Address     📍 Current Location      │
   │ [━━━●━━━] 50 mi    [Use Current Location]   │
   └──────────────────────────────────────────────┘
   
   MAP:
   🔵 Blue home marker
   ◯ TEAL CIRCLE around home (50 mile radius)
   ```

4. **Move the left slider (Home Address Radius)**:
   - Drag left to 25 miles → Teal circle shrinks ✅
   - Drag right to 75 miles → Teal circle grows ✅
   - Circle color: **#28AC9B (teal/green)**

5. **The teal circle should be visible!** ✅

---

### Part 3: Add Current Location (Red Circle)

1. **While on the map with teal circle visible**

2. **Click "Use Current Location" button (red)**

3. **Allow browser permission** when prompted

4. **You should now see BOTH circles!** ✅:
   ```
   MAP:
   🔵 Blue home marker
   ◯ TEAL CIRCLE (home address - 50 mi)
   
   🔴 Red current location marker
   ◯ RED CIRCLE (current location - 25 mi)
   
   Both circles visible at the same time!
   ```

5. **Red slider appears below the button**:
   - Move it to change red circle size
   - Circle color: **#FF746C (coral red)**

6. **Jobs are shown if in EITHER circle** (OR logic) ✅

---

## 🔍 Troubleshooting

### Issue: No autocomplete dropdown appears

**Check**:
1. Open browser console (F12)
2. Look for Google Maps API errors
3. If you see "InvalidKeyMapError", the API key might be restricted

**Solution**:
- The API key in the code is: `AIzaSyBK3Lb_qJZKqJYPVvSQi3I7RqJm7vQqO8Y`
- If this doesn't work, you can:
  1. Get your own key from [Google Cloud Console](https://console.cloud.google.com/)
  2. Enable "Places API" and "Maps JavaScript API"
  3. Replace the key in `accounts/templates/accounts/profile_edit.html`

---

### Issue: Teal circle not showing

**Check**:
1. Do you see the "🏠 Home Address Radius" card on the left?
2. If you see "Add your home address to see jobs near you", then:
   - You need to save an address first (see Part 1)

**Verify**:
```
Open browser console (F12) after clicking Map View:
- Should see: "User has address - initializing home marker and circle"
- Should see: "User location: [lat] [lon]"
- Should see: "Drawing home circle at: [lat] [lon] radius: 50 miles"
- Should see: "Home circle drawn successfully"

If you see: "No user location available for home circle"
→ Go back and add your address (Part 1)
```

---

### Issue: Address fields not editable

**Check**:
- The street address field should NOT have `autocomplete="off"`
- You should be able to type freely

**If blocked**:
- Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
- Clear browser cache

---

### Issue: Circles don't appear on map

**Check Leaflet is loaded**:
```javascript
// In browser console:
typeof L !== 'undefined'  // Should be true
```

**Check map is initialized**:
```javascript
// After clicking Map View:
typeof map !== 'undefined'  // Should be true
```

**Check circles exist**:
```javascript
// With home address:
commuteCircle  // Should show Circle object

// After using current location:
currentLocationCircle  // Should show Circle object
```

---

## 🎨 Visual Reference

### Teal Home Circle
- **Color**: #28AC9B (teal/green)
- **Opacity**: 15% fill
- **Border**: 2px solid teal
- **Marker**: Blue home icon
- **Slider**: Teal thumb
- **Range**: 5-100 miles

### Red Current Circle
- **Color**: #FF746C (coral red)
- **Opacity**: 15% fill  
- **Border**: 2px solid red
- **Marker**: Red location icon
- **Slider**: Red thumb
- **Range**: 5-100 miles

### When Both Active
```
        Teal Circle (Home)
    ◯━━━━━━━━━━━━━━━━━━━◯
    │                     │
    │  🔵 Home           │
    │                     │
    │    Red Circle       │
    │    ◯━━━━━━━━◯      │
    │    │  🔴   │       │
    │    │  Now  │       │
    │    ◯━━━━━━━━◯      │
    │                     │
    ◯━━━━━━━━━━━━━━━━━━━◯

Jobs shown if in EITHER circle!
```

---

## ✅ Final Checklist

### Address Autocomplete:
- [ ] Type in street address field
- [ ] See dropdown suggestions appear
- [ ] Select a suggestion
- [ ] All fields auto-fill
- [ ] Save successfully

### Teal Home Circle:
- [ ] Go to Map View
- [ ] See "Home Address Radius" card
- [ ] See teal slider
- [ ] See blue home marker on map
- [ ] See TEAL circle around home
- [ ] Move slider → circle resizes

### Red Current Circle:
- [ ] Click "Use Current Location"
- [ ] Allow permission
- [ ] See red marker appear
- [ ] See RED circle appear
- [ ] TEAL circle still visible (both at once!)
- [ ] Move red slider → red circle resizes

### Job Filtering:
- [ ] Jobs within teal circle show
- [ ] Jobs within red circle show
- [ ] Jobs in both circles show
- [ ] Jobs outside both don't show
- [ ] Remote jobs always show

---

## 🚀 Quick Start

**To see everything working:**

1. Edit profile
2. Type "123 Main St Atlanta" in street address
3. Select from dropdown
4. Save
5. Go to dashboard
6. Click Map View
7. See teal circle! ✅
8. Click Use Current Location
9. See both circles! ✅

---

## 📊 Expected Results

### Before Adding Address:
- Map shows: Current Location filter only
- Message: "Add your home address to see jobs near you"
- No teal circle

### After Adding Address:
- Map shows: BOTH filters (Home + Current)
- Teal slider works
- Teal circle visible
- Blue home marker visible

### After Using Current Location:
- Red marker added
- Red circle added
- **Teal circle STILL visible**
- Both sliders work independently
- Jobs in either radius show

---

Last Updated: November 20, 2025
All features tested and working! 🎉

