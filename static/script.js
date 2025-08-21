function searchUser() // Used in user list to search for specific user
{
    // Declare variables
    const input = document.getElementById('search_name').value;
    const ul = document.getElementById("userlist");
    const posts = ul.getElementsByTagName('li'); // Get all posts in an array

    for (let i = 0; i < posts.length; i++) // Loops trough all posts and checks for each if they contain searched term and shows it if it does
    {
        if (posts[i].textContent.includes(input))
        {
            posts[i].style.display = ""; // Shows it
        }
        else
        {
            posts[i].style.display = "none"; // Hides it
        }
    }
}

function searchPost() // Used to search posts by title and by person who posted it 
{
    // Declare variables
    // There are 2 inputs because there are 2 search fields one where you search for titles and 1 where you search for authors
    const inputTitle = document.getElementById('search_title').value; 
    const inputAuthor = document.getElementById('search_author').value;
    const post_list = document.getElementById("posts");
    const posts = post_list.getElementsByClassName('card'); // Get all posts
    // Because data for title and author is not same (obviously) we have 2 get 2 arrays of elements we will compare to
    const elementsTitle = post_list.getElementsByClassName('post_title');
    const elementsAuthor = post_list.getElementsByClassName('post_author');
    
    for (let i = 0; i < posts.length; i++) // Loops trough all searched for things(titles and authors) and checks for each if they contain searched term and shows it if it does
    {
        if (elementsTitle[i].textContent.includes(inputTitle) && elementsAuthor[i].textContent.includes(inputAuthor))
        {
            posts[i].style.display = ""; // Shows it
        }
        else
        {
            posts[i].style.display = "none"; // Hides it
        }
    }
}

function switchImage(currentIndex, targetedIndex, postID) {
    // Hide current image
    document.getElementById(`image${postID}_${currentIndex}`).hidden = true; // Hide current image
    
    // Find next available image in the correct direction
    const direction = currentIndex < targetedIndex ? 1 : -1; // If searched for image has a bigger index or smaller
    
    while (true) { // Loop trough images until you find the colest one that fits requirements in that case display it
        const image = document.getElementById(`image${postID}_${targetedIndex}`);
        if (image) {
            image.hidden = false;
            break;
        }
        targetedIndex += direction;
    }
}

function react(action, username, postID, commentID = null){
    // Action is either like or dislike
    // Username is a person who reacted 
    if (username === '') // If user not logged in
    {
        alert('Please log in to do that');
        return;
    }
    let link; // Used to only need 1 link no matter if comment is reacted to or post
    let id; // Main id used later for coloring button
    if(commentID !== null){ // If comment exists
        link = `/react/${postID}/${commentID}`;
        id = commentID;
    }else{ // If post
        link = `react/${postID}`;
        id = postID;
    }
    // update is a js promise that posts to link with JSON type data
    const update = fetch(link,
    {
        method: 'POST',
        headers: {'Content-Type': 'application/json; charset=utf-8'},
        body: JSON.stringify(action)
    }
    )
    .then(response => response.json()) // response.json returns yet another promise
    .then(data => // 
    {
        document.getElementById(`likes${id}`).innerText = data.like_count; // Id of selected element either a post or a comment gets a correct amount of likes and dislikes
        document.getElementById(`dislikes${id}`).innerText = data.dislike_count;
        // Corectly colours button depending on if user has likes a post/comment or not
        if (data.liked_by.includes(username)) 
        {
            document.getElementById(`like_${id}`).classList.add('btn-dark');
            document.getElementById(`dislike_${id}`).classList.remove('btn-dark');
        }
        else if(data.disliked_by.includes(username))
        {
            document.getElementById(`like_${id}`).classList.remove('btn-dark');
            document.getElementById(`dislike_${id}`).classList.add('btn-dark');
        }
        else
        {  
            document.getElementById(`like_${id}`).classList.remove('btn-dark');
            document.getElementById(`dislike_${id}`).classList.remove('btn-dark');
        }
    }
    )
}

function addComment(postID, parentCommentID, indent){
    // If comment to a post directly parentCommentID is 0
    // Indent is how deep new comment will be indented
    const textArea = document.getElementById(`commentContent_${parentCommentID}`);
    const commentContent = textArea.value;
    textArea.value = ''; // Clears text area

    // If submitted empty
    if (!commentContent) {
        alert('Please enter a comment before submitting.');
        return;
    }

    // Disable button to prevent double submission while submission is being processed
    const submitButton = document.getElementById(`add_${parentCommentID}`);
    submitButton.disabled = true;
    submitButton.textContent = 'Posting...';

    console.log(commentContent);
    const add = fetch(`/view/post/${postID}/${parentCommentID}`,
    {
        method: 'POST',
        headers: {'Content-Type': 'application/json; charset=utf-8'},
        body: JSON.stringify(commentContent) // Return a list of strings (lines) of a comment 
    }
    )
    .then(response => response.json()) // Response was received as JSON from server so make it to a dict(object(hash table))
    .then(data => // Data is a dict of comment id and it's owner
    {
        document.getElementById(`placeholder_${parentCommentID}`).insertAdjacentHTML('beforeend', // Dynamically add a comment (flask app added it to a db as well)
        `      
            <div> 
                <div style="margin-left: ${indent}%;" id="comment_${data['id']}">
            
                    <p>${data['username']}, Posted a few moments ago
                    Likes: <span id="likes${data['id']}">0</span> Dislikes: <span id="dislikes${data['id']}">0</span></p>

                    <div class="preserve">${commentContent}</div>

                    <button class="btn" id="like_${data['id']}" name="reaction" value="like" onclick="react('like', '${data['username']}', ${postID}, ${data['id']})">Like</button>
                    <button class="btn" id="dislike_${data['id']}" name="reaction" value="dislike" onclick="react('dislike', '${data['username']}', ${postID}, ${data['id']})">Dislike</button>

                    <textarea name="comment" style="display: inline-block;" placeholder="Add a reply" id="commentContent_${data['id']}"></textarea>
                    <button onclick="addComment(${postID}, ${data['id']}, ${indent+2})" style="display: inline-block;" id="add_${data['id']}">Reply</button>

                    <form method="get" action="/edit_comment/${postID}/${data['id']}">
                        <button type="submit">Edit</button>
                    </form>

                    <form method="post" action="/remove/${postID}/${data['id']}">
                        <button type="submit">Remove</button>
                    </form>
                    
                </div>

                <div id="placeholder_${data['id']}"></div>
            </div> 
        ` // Placeholder div is for a new comment to be added to
        );
    }
    );
    submitButton.disabled = false; // Since post was added successfully make button for submitting work again
    submitButton.textContent = 'Add';
}