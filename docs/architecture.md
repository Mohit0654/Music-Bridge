# Architecture Overview

Music Bridge follows a modular and extensible architecture designed for cross-platform playlist conversion.

- **Extractor**  
  Responsible for retrieving playlist data from the source platform.  
  In the current demo, this uses mock Spotify data due to developer access limits.

- **Converter**  
  Transforms raw playlist data into a platform-independent format  
  (e.g., "Song Name – Artist"), making it reusable across services.

- **Creator**  
  Handles target platform integration by:
  - Authenticating users via OAuth
  - Creating playlists
  - Searching and adding matching tracks automatically

This separation allows Music Bridge to easily support additional platforms in the future.
