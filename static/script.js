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

function switchImage(currentIndex, targetedIndex, postId){ // Used to switch between images on posts if a post have more than one
    document.getElementById(`image${currentIndex}_${postId}`).hidden = true;
    document.getElementById(`image${targetedIndex}_${postId}`).hidden = false;
}

function react(action, username, post_id, comment_id = null){
    // Action is either like or dislike
    // Username is a person who reacted 
    if (username === '') // If user not logged in
    {
        alert('Please log in to do that');
        return
    }
    let link; // Used to only need 1 link no matter if comment is reacted to or post
    let id; // Main id used later for coloring button
    if(comment_id !== null){ // If comment exists
        link = `/react/${post_id}/${comment_id}`;
        id = comment_id;
    }else{ // If post
        link = `react/${post_id}`;
        id = post_id;
    }
    // update is a js promise that posts to link with JSON type data
    const update = fetch(link,
    {
        method: 'POST',
        headers: {'Content-Type': 'application/json; charset=utf-8'},
        body: JSON.stringify
        ({
            action: action,
            username: username        
        })
    }
    )
    update.then(response => response.json()) // response.json returns yet another promise
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
