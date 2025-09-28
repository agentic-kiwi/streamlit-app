## Phase 1: Basic Streamlit Setup

```
bash

# 1. Install Streamlit
pip install streamlit

# 2. Create web interface file
touch streamlit_app.py

# 3. Basic page structure
- [ ] Import existing chain functions
- [ ] Create sidebar for navigation
- [ ] Add topic selector
- [ ] Implement basic chat interface

```

## Phase 2: Mode Integration

```
python

# 4. Integrate analysis modes
- [ ] Basic Q&A mode
- [ ] Structured analysis display
- [ ] Parallel analysis results formatting
- [ ] Conversational mode with session memory

```
## Phase 3: Enhanced UX

```
pyhton

# 5. Improve interface
- [ ] Message history display
- [ ] Loading indicators
- [ ] Error handling for API failures
- [ ] Clear conversation button

```

## Phase 4: Testing & Polish

```
bash

# 6. Validation
- [ ] Test all four modes in web interface
- [ ] Verify topic switching works
- [ ] Check session persistence within single session
- [ ] Run: streamlit run streamlit_app.py

```

## File Structure After Changes:

```
topic-learning-assistant/
├── streamlit_app.py          # New web interface
├── app.py                    # Keep existing CLI
├── config/
├── chains/
├── models/
└── utils/

```