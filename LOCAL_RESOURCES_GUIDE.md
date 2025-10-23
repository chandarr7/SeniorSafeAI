# Local Resources Lookup Feature

## Overview

SeniorSafe AI now includes an **automatic local resource lookup feature** that helps users find local law enforcement, state consumer protection offices, and federal agencies to report cybercrimes based on their ZIP code.

## Features

### Automatic ZIP Code Detection
- System automatically detects ZIP codes in user messages
- Supports both 5-digit (e.g., 10001) and ZIP+4 format (e.g., 10001-1234)
- Intelligent parsing that recognizes ZIP codes in natural language

### Comprehensive Resource Database
The system provides information for:

#### State-Level Resources
- **All 50 states + DC**: State Attorney General Consumer Protection offices
- Direct phone numbers and websites for each state
- Specific contact information for fraud and cybercrime reporting

#### Federal Resources
- **Federal Trade Commission (FTC)** - General fraud and identity theft
- **FBI Internet Crime Complaint Center (IC3)** - Internet crimes
- **IdentityTheft.gov** - Identity theft recovery
- **U.S. Postal Inspection Service** - Mail fraud
- **IRS Identity Protection** - Tax-related identity theft
- **Social Security Administration** - SSN fraud

#### Local Resources
- Local police department guidance
- Links to find local government contacts

### Smart Keyword Detection
The system recognizes when users are asking for help finding local resources through keywords like:
- "local"
- "police"
- "report"
- "where"
- "agency"
- "department"
- "office"
- "near me"
- "ZIP code"

## How It Works

### User Flow

1. **User asks for local help**
   ```
   User: "Where can I report this scam?"
   System: "To find local resources in your area, I'll need your ZIP code..."
   ```

2. **User provides ZIP code**
   ```
   User: "My ZIP code is 10001"
   System: [Provides comprehensive list of resources for NY]
   ```

3. **Or user provides ZIP code directly**
   ```
   User: "I need help reporting this. I'm in 90210"
   System: [Automatically detects ZIP code and provides CA resources]
   ```

### Conversation Starter

A dedicated conversation starter is available:
- **"Find Local Help"** - Guides users to provide their ZIP code for local resources

## Technical Implementation

### Module: `local_resources.py`

#### Classes

**ZIPCodeValidator**
- Validates ZIP code format
- Extracts 5-digit ZIP from ZIP+4 format
- Ensures data quality

**ZIPToStateMapper**
- Maps ZIP code ranges to state abbreviations
- Covers all US states and territories
- Fast lookup using range-based algorithm

**LocalResourceDatabase**
- Comprehensive database of state consumer protection offices
- Federal agency contact information
- Structured data format for easy updates

**LocalResourceFormatter**
- Formats resources into readable markdown
- Groups by type (State, Federal, Local)
- Includes actionable next steps

### Integration Points

#### Chat UI Integration (`seniorsafe_chat_ui_v1.py`)
- `extract_zip_code()` - Extracts ZIP from messages
- `check_for_local_resources_request()` - Detects resource requests
- Automatic response when ZIP code detected
- Prompt for ZIP code when not provided

## Example Outputs

### Example 1: New York (ZIP 10001)
```markdown
## Local Resources for ZIP Code 10001 (NY)

### State Resources
**New York Attorney General Bureau of Consumer Frauds**
- Phone: 1-800-771-7755
- Website: https://ag.ny.gov/bureau/consumer-frauds-bureau

### Federal Resources
[Lists all 6 federal agencies with contact info]

### Local Law Enforcement
[Guidance on contacting local police]

### What to Do Next:
1. Start with your state consumer protection office
2. File a report with the FTC
3. Report to IC3 if internet crime
4. Contact local police for serious crimes
5. Keep records of all reports
```

### Example 2: California (ZIP 90210)
```markdown
## Local Resources for ZIP Code 90210 (CA)

### State Resources
**California Attorney General Public Inquiry Unit**
- Phone: 1-800-952-5225
- Website: https://oag.ca.gov/contact/...
```

## Usage Scenarios

### Scenario 1: Identity Theft Victim
```
User: "Someone stole my identity. Who do I call?"
AI: "I can help you find local resources. What's your ZIP code?"
User: "60601"
AI: [Provides Chicago/Illinois resources including state AG and federal agencies]
```

### Scenario 2: Tech Support Scam
```
User: "I was scammed by fake tech support. I'm in 33101"
AI: [Automatically detects ZIP code for Miami, FL and provides:
     - Florida Attorney General info
     - FTC reporting
     - FBI IC3
     - Local police guidance]
```

### Scenario 3: Reporting Guidance
```
User: "I need to report this crime. Where do I start?"
AI: [Explains reporting process and asks for ZIP code]
User: "My ZIP is 02101"
AI: [Provides Boston/Massachusetts resources]
```

## Data Coverage

### Geographic Coverage
- **All 50 US States**: Complete coverage with verified contact information
- **District of Columbia**: Full coverage
- **ZIP Code Range**: 00501 - 99999

### Information Accuracy
- All phone numbers verified (as of October 2025)
- Websites checked for accuracy
- Regular updates recommended for ongoing accuracy

## Maintenance

### Updating Resources

To update contact information:

1. **Edit `local_resources.py`**
2. **Update the `STATE_CONSUMER_OFFICES` dictionary**
   ```python
   'CA': {
       'name': 'California AG Office',
       'phone': '1-800-XXX-XXXX',
       'website': 'https://...',
       'description': '...'
   }
   ```
3. **Test with sample ZIP codes**
4. **Commit changes**

### Adding New Resources

To add new types of resources (e.g., local FBI offices):

1. Create new dictionary in `LocalResourceDatabase`
2. Add to `get_resources_by_state()` method
3. Update formatter to handle new type
4. Test thoroughly

## Privacy & Security

### Privacy Considerations
- ZIP codes are processed locally
- No data is stored or transmitted externally
- No personally identifiable information is collected
- ZIP codes are only used for resource lookup

### Data Security
- Static database (no external API calls)
- No network requests for ZIP lookup
- All data embedded in the application

## Testing

### Test Cases

Run the test script:
```bash
cd Seniorsafe_LD
python3 local_resources.py
```

This tests multiple ZIP codes across different states:
- 10001 (New York)
- 90210 (California)
- 60601 (Illinois)
- 33101 (Florida)
- 02101 (Massachusetts)

### Manual Testing

Test in the chat interface:
1. Start the application
2. Click "Find Local Help" starter
3. Provide a test ZIP code
4. Verify all resources are displayed correctly

## Troubleshooting

### Common Issues

**Issue**: ZIP code not recognized
- **Solution**: Ensure 5-digit format, no spaces or special characters

**Issue**: No resources found
- **Solution**: Verify ZIP code is valid US ZIP code in range 00501-99999

**Issue**: State not mapping correctly
- **Solution**: Check ZIP code range in `ZIP_RANGES` dictionary

## Future Enhancements

Potential improvements:

1. **City-Level Resources**
   - Add major city police departments
   - Local FBI field offices by city

2. **County Resources**
   - County sheriff departments
   - County consumer protection offices

3. **Specialized Resources**
   - Elder abuse hotlines
   - Financial crimes task forces
   - Cybersecurity centers

4. **Multi-Language Support**
   - Translate resource information
   - Spanish, Chinese, other common languages

5. **Resource Ratings**
   - Response time information
   - User feedback on helpfulness
   - Best practices for each agency

6. **API Integration**
   - Real-time data from government APIs
   - Automatic updates
   - Hours of operation

## Support

For issues with the local resources feature:
1. Check ZIP code format (5 digits)
2. Verify state mapping in code
3. Review error messages
4. Check logs for debugging information

## Compliance

This feature helps users comply with reporting requirements:
- Encourages reporting to appropriate authorities
- Provides multiple reporting channels
- Includes both state and federal options
- Promotes official government resources

---

**Last Updated:** October 23, 2025
**Version:** 1.0
**Author:** SeniorSafe AI Development Team
