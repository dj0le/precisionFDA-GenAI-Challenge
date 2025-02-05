Move new CLI version to FastAPI / UI version




4. **Update Chat Endpoint**
   - Implement new LLM engine
   - Add metadata collection
   - Update response format to match CLI JSON structure
   - Basic session management

### Phase 3: Enhanced Features
5. **Improve Error Handling and Logging**
   - Structured error responses
   - Enhanced logging
   - Basic monitoring

6. **Add Progress Monitoring**
   - Add websocket support
   - Implement progress tracking
   - Add status endpoints




2. Response Structure
   - Modify the API responses to include the additional metadata we're collecting in the CLI version (processing time, tokens, sources)
   - Create new Pydantic models that match the JSON structure we developed for the CLI

3. Session Management
   - Enhance the current UUID-based session management to better handle chat history
   - Consider adding websocket support for real-time communication with the JavaScript frontend

4. Document Processing
   - Update the document processing pipeline to use the new `DocumentProcessor` class
   - Implement better error handling and progress tracking for document uploads

5. API Endpoints
   - Add new endpoints to support:
     - Progress monitoring for long-running operations
     - Batch operations for multiple questions
     - Document processing status
     - More detailed error responses
   - Add CORS support for the JavaScript frontend

6. Frontend Considerations
   - Add CORS middleware to FastAPI for JavaScript frontend access
   - Implement proper error handling that returns JSON responses
   - Add endpoints for frontend-specific needs (authentication, user preferences, etc.)
   - Consider adding API documentation using FastAPI's built-in Swagger UI

7. Monitoring and Logging
   - Integrate the detailed metrics collection we added in the CLI version
   - Add structured logging for better debugging
   - Consider adding performance monitoring endpoints

8. Configuration
   - Create a unified configuration system that works for both CLI and API
   - Add environment-based configuration for different deployment scenarios

9. Testing
   - Add API-specific tests
   - Include integration tests for the JavaScript frontend
   - Add performance testing endpoints

The main architectural change would be moving from a simple request-response pattern to a more sophisticated system that provides:
- Detailed metadata about operations
- Progress monitoring
- Better error handling
- Real-time updates
- Structured responses that match our CLI JSON format
