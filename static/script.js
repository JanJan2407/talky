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