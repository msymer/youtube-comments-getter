# Youtube Comments Getter
The Python script to write comments form Youtube video with some metadata do the file in specific format.
## Configuration
Set the configuration in the config.json file.
- `apiKey`: Your key to the Google API services
- `formatting`: Output file format style
- `outputExtension`: Output file extension
- `commentsApiUrl`: URL for Youtube comments API GET call. The url must contain tags `{api_key}`, `{video_id}` and `{nextPageToken}`.
- `commentsCount`: Max count of comments in the output file in hundreds. (200 = 200; 201 = 300)

## Formatting
You can set the formatting for output file in the config file.
### Sections
- `<RR> something <RR>`: The record format section - section for the comment record data. The section must contain `<SS>` pair tag.
- `<SS> separator format <SS>`: The separator section. The section must be inside the `<RR>`. The separator is inserted only when there is more than 1 record.

### Record data
- `<CMT>`: The comment text. The comment can not be a reply comment.
- `<RCMT>`: The reply comment text.
- `<ATH>`: The author of the comment.
- `<RAT>`: Count of the comment likes.
- `<NL>`: Insert new line.
- `<DAT>`: The date of the comment last edit.
- `<REP>`: Count of the reply comments.
- `<ID>`: The id of the comment.
- `<PAR>`: The id of the parent comment if is reply comment.

### Example
**Config file:** `... "formatting": "Comments:<NL><RR><ATH>: <CMT><SS>,<NL><SS><RR>" ...`

**Output file:**
```
Comments:
Alice: This is my comment,
Bob: And this is my comment
```
## How to run?
The scripts were developed in Python v3.7.3.

To run the scripts you need to specifi the argument with the youtube video id.
```
python3 comments-getter.py JoT8GZHyEgQ
```
