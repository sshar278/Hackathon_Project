source "github_webhook"
bucket "events"
bucket "diffs"
bucket "reviews"
endpoint "notify" path "/api/notify" method POST
endpoint "review" path "/api/review" method GET

on "push" from "github_webhook" do
  write to "events"
  let meta = transform "extract_diff" with event.body
  let review = transform "review_with_claude" with meta
  write to "reviews" with review
  post to "/api/notify" with review
end

