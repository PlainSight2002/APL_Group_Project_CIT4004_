code = """

#-- *************************************************************
#-- Source Code written in the Reservation System Language
#-- *************************************************************

#--book reservation @P "Palace" for "Darrell King" on 2024-12-10 from "Kingston" to "Maximum Bay" @T "5:00pm"..
#--book reservation @P "Windex" for "Shawn James" on 2025-03-10 from "Clarendon" to "Mandeville" @T "3:40pm"..
#--book reservation @P "Palace" for "Chantel Smith" on 2025-06-15 from "Old Harbour" to "James Hill" @T "6:10pm"..

#--view reservation :: "Paid"..

#--cancel reservation @"Windex" for "Shawn James"..
#--cancel ticket @P "M10 Restaurant" for "Simone Smith" :: "2"..

#--confirm reservation @"Palace" for "Chantel Smith" :: 6..

#--pay reservation @"Palace" for "Darrell King" :: 7..

list "Knutsford express schedule jamaica"..

#--book ticket @P "M10 Restaurant" for "Simone Smith" on 2025-08-15 from "Old Harbour" to "James Hill" @T "6:10pm"..

#--book ticket @P "M10 Restaurant" for "Kerry Brown" on 2025-08-15 from "Old Harbour" to "James Hill" @T "6:10pm"..

#--book ticket @P "M10 Restaurant" for "Kenny James" on 2025-08-15 from "Old Harbour" to "James Hill" @T "6:30pm"..

#--output("Testing print statement")..

#--book reservation @P "Grey Hound" for "Paul Kingston" on 2024-12-10 from "Kingston" to "Clarendon" @T "6:10pm"..

#--cancel ticket @P "M10 Restaurant" for "Simone Smith"..
#--cancel ticket @P "M10 Restaurant" for "Simone Smith" :: "2"..

#--Used to view a list of tickets with a specific status (Active or Cancelled)
#--view ticket :: "Active"..

#--view ticket for "Simone Smith"..

#--declare string _PersonName = "Peter Grant"..
#--book reservation @P "Grey Hound" for _PersonName on 2024-12-10 from "Kingston" to "Clarendon" @T "6:10pm"..

#--Book without a from location and start location
#--book reservation @P "Burger King" for "Simmon Sims" on 2024-12-10 @T "6:10pm"..



declare int _COUNT = 3..

repeatif (_COUNT >= 0){
    _COUNT = (_COUNT - 1)..
    output("This is a repeated output")..
}
output(_COUNT)..

"""
