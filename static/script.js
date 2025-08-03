function searchUser() // Used in userlist to search for specific user
{
    // Declare variables
    const input = document.getElementById('search_name').value;
    const ul = document.getElementById("userlist");
    const usernames = ul.getElementsByTagName('li'); // Get all usernames in an array

    for (let i = 0; i < usernames.length; i++) // Loops trough all usernames and checks for each if they contain searched term and shows it if it does
    {
        if (usernames[i].textContent.includes(input))
        {
            usernames[i].style.display = ""; // Shows it
        }
        else
        {
            usernames[i].style.display = "none"; // Hides it
        }
    }
}