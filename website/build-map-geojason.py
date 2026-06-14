#!/usr/bin/env python3
import os
import re
import json


# Regex pattern to match geo-location markdown links with optional tags
# Format: [name](geo:lat,lon) tag:tagname
GEO_LINK_RE = re.compile(
    r'\[([^\]]+)\]\(geo:([0-9\.\-]+),([0-9\.\-]+)\)(?:\s+tag:([a-zA-Z0-9_-]+))?', re.IGNORECASE
)

def extract_features_from_md(md_path):
  """Extract geographic features from markdown file and convert to GeoJSON format"""
  features = []
  with open(md_path, encoding='utf-8') as f:
    for line in f:
      # find all the geo-location links in each line
      for match in GEO_LINK_RE.finditer(line):
        name = match.group(1).strip()  # Extract location name from brackets
        lat = float(match.group(2))
        lon = float(match.group(3))
        tag = match.group(4).strip() if match.group(4) else "" # Extract optional tag

        # create a GeoJson feature object for each location
        features.append({
                    "type": "Feature",
                    "properties": {
                        "name": name,
                        "iconType": tag  # Use tag as iconType for map visualization
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat]  # GeoJSON uses [longitude, latitude] order
                    }
                })
    return features
  
def main():
  """Processes all markdown files in the dir and generates GeoJson maps"""
  content_root = os.path.join(os.path.dirname(__file__), "content")

  # Walk through all the dirs and subdirs
  for dirpath, _, filenames in os.walk(content_root):
    all_features = []

    # process each markdown file in the current dir
    for fname in filenames:
      if fname.endswith('.md'):
        md_path = os.path.join(dirpath, fname)
        features = extract_features_from_md(md_path)
        all_features.extend(features)
    
    # if there are any geo features, create a GeoJSON file
    if all_features:
      geojson = {
        "type": "FeatureCollection",
        "features": all_features
      }

      # Write GeoJSON file to the same dir as the markdown files
      geojson_path = os.path.join(dirpath, "map.geojson")
      with open(geojson_path, "w", encoding='utf-8') as f:
        json.dump(geojson, f, indent=2)

    print(f"Wrote {len(all_features)} features to {geojson_path}")

if __name__ == "__main__":
  main()