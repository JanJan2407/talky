function searchUser() //used in userlist to search for specific user
{
    // Declare variables
    const input = document.getElementById('search_name').value;
    const ul = document.getElementById("userlist");
    const usernames = ul.getElementsByTagName('li'); // get all usernames in an array

    for (let i = 0; i < usernames.length; i++) //loops trough all usernames and checks for each if they contain searched term and shows it if it does
    {
        if (usernames[i].textContent.includes(input))
        {
            usernames[i].style.display = ""; //shows it
        }
        else
        {
            usernames[i].style.display = "none"; //hides it
        }
    }
}