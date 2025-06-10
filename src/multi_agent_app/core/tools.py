import ast
from langchain_core.tools import tool
from langchain_community.utilities.sql_database import SQLDatabase
from .db import init_memory_engine

_engine = init_memory_engine()
db = SQLDatabase(_engine)

@tool
def get_albums_by_artist(artist: str):
    """
    Get albums by an artist.
    Returns JSON rows { "Title": ..., "Name": ... }.
    """
    return db.run(
        f"""
        SELECT Album.Title, Artist.Name 
        FROM Album 
        JOIN Artist ON Album.ArtistId = Artist.ArtistId 
        WHERE Artist.Name LIKE '%{artist}%';
        """,
        include_columns=True
    )

@tool
def get_tracks_by_artist(artist: str):
    """
    Get songs/tracks by an artist.
    """
    return db.run(
        f"""
        SELECT Track.Name as SongName, Artist.Name as ArtistName 
        FROM Album 
        LEFT JOIN Artist ON Album.ArtistId = Artist.ArtistId 
        LEFT JOIN Track ON Track.AlbumId = Album.AlbumId 
        WHERE Artist.Name LIKE '%{artist}%';
        """,
        include_columns=True
    )

@tool
def get_songs_by_genre(genre: str):
    """
    Fetch songs matching a genre (up to 8).
    """
    genre_ids = db.run(
        f"SELECT GenreId FROM Genre WHERE Name LIKE '%{genre}%'"
    )
    if not genre_ids:
        return f"No songs found for {genre}"

    # parse the result (list of lists)
    ids = ast.literal_eval(genre_ids)
    if not ids:
        return f"No songs found for {genre}"

    joined_ids = ", ".join(str(row[0]) for row in ids)
    query = f"""
        SELECT Track.Name as SongName, Artist.Name as ArtistName
        FROM Track
        LEFT JOIN Album  ON Track.AlbumId  = Album.AlbumId
        LEFT JOIN Artist ON Album.ArtistId = Artist.ArtistId
        WHERE Track.GenreId IN ({joined_ids})
        GROUP BY Artist.Name
        LIMIT 8;
    """
    songs = db.run(query, include_columns=True)
    if not songs:
        return f"No songs found for {genre}"
    return songs

@tool
def check_for_songs(song_title: str):
    """Check if a song exists by partial name."""
    return db.run(
        f"SELECT * FROM Track WHERE Name LIKE '%{song_title}%';",
        include_columns=True
    )

@tool
def get_invoices_by_customer_sorted_by_date(customer_id: str):
    """
    Return all invoices for a customer, newest first.
    """
    return db.run(
        f"""
        SELECT *
        FROM Invoice
        WHERE CustomerId = {customer_id}
        ORDER BY InvoiceDate DESC;
        """,
        include_columns=True,
    )

@tool
def get_invoices_sorted_by_unit_price(customer_id: str):
    """
    Same invoices, sorted by highest UnitPrice item first.
    """
    q = f"""
        SELECT Invoice.*, InvoiceLine.UnitPrice
        FROM Invoice
        JOIN InvoiceLine ON Invoice.InvoiceId = InvoiceLine.InvoiceId
        WHERE Invoice.CustomerId = {customer_id}
        ORDER BY InvoiceLine.UnitPrice DESC;
    """
    return db.run(q, include_columns=True)

@tool
def get_employee_by_invoice_and_customer(invoice_id: str, customer_id: str):
    """
    Who helped with a specific invoice?
    """
    q = f"""
        SELECT Employee.FirstName, Employee.Title, Employee.Email
        FROM Employee
        JOIN Customer ON Customer.SupportRepId = Employee.EmployeeId
        JOIN Invoice  ON Invoice.CustomerId     = Customer.CustomerId
        WHERE Invoice.InvoiceId = {invoice_id}
          AND Invoice.CustomerId = {customer_id};
    """
    info = db.run(q, include_columns=True)
    return info or f"No employee found for Invoice {invoice_id}"

MUSIC_TOOLS = [get_albums_by_artist,
               get_tracks_by_artist,
               get_songs_by_genre,
               check_for_songs]

INVOICE_TOOLS = [
    get_invoices_by_customer_sorted_by_date,
    get_invoices_sorted_by_unit_price,
    get_employee_by_invoice_and_customer,
]